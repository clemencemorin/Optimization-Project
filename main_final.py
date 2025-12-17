#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, Tuple

import networkx as nx
import matplotlib.pyplot as plt


# =========================
# Data structures
# =========================

@dataclass(frozen=True)
class EdgeSpec:
    u: str
    v: str
    capacity: int
    length: float
    kind: str  # "corridor" or "stairs"


def default_edges() -> list[EdgeSpec]:
    def L(kind: str) -> float:
        return {"corridor": 12.0, "stairs": 10.0}[kind]

    return [
        EdgeSpec("N", "A", 120, L("corridor"), "corridor"),
        EdgeSpec("A", "B", 60, L("corridor"), "corridor"),
        EdgeSpec("A", "C", 60, L("corridor"), "corridor"),
        EdgeSpec("B", "S1", 40, L("corridor"), "corridor"),
        EdgeSpec("C", "S2", 40, L("corridor"), "corridor"),
        EdgeSpec("S1", "D", 40, L("stairs"), "stairs"),
        EdgeSpec("S2", "D", 40, L("stairs"), "stairs"),
        EdgeSpec("D", "S", 120, L("corridor"), "corridor"),
        EdgeSpec("B", "C", 20, 8.0, "corridor"),
        EdgeSpec("C", "B", 20, 8.0, "corridor"),
        EdgeSpec("S1", "S2", 15, 6.0, "corridor"),
        EdgeSpec("S2", "S1", 15, 6.0, "corridor"),
    ]


# =========================
# Graph construction
# =========================

def build_graph(alpha_stairs: float, v: float) -> nx.DiGraph:
    """
    Build directed graph with:
    - capacity (people/min)
    - weight = travel time cost (scaled x10 for integer min-cost flow)
    """
    G = nx.DiGraph()

    for e in default_edges():
        gamma = alpha_stairs if e.kind == "stairs" else 0.0
        T = e.length / v + gamma
        G.add_edge(
            e.u,
            e.v,
            capacity=e.capacity,
            weight=int(round(T * 10)),
            kind=e.kind,
        )
    return G


# =========================
# Flow computations
# =========================

def compute_max_flow(G: nx.DiGraph) -> Tuple[int, Dict]:
    return nx.maximum_flow(G, "N", "S", capacity="capacity")


def min_cost_for_flow(G: nx.DiGraph, flow_value: int) -> Tuple[int, Dict]:
    H = G.copy()
    for n in H.nodes():
        H.nodes[n]["demand"] = 0

    H.nodes["N"]["demand"] = -flow_value
    H.nodes["S"]["demand"] = flow_value

    flow = nx.min_cost_flow(H, capacity="capacity", weight="weight")
    cost = sum(flow[u][v] * H[u][v]["weight"] for u in flow for v in flow[u])
    return cost, flow


def print_positive_flows(flow: Dict) -> None:
    for u, nbrs in flow.items():
        for v, f in nbrs.items():
            if f > 0:
                print(f"  {u} -> {v}: {f}")


# =========================
# Visualization
# =========================

def draw_graph(G, flow=None, title="", filename=None):
    pos = {
        "N": (0, 4),
        "A": (0, 3),
        "B": (-2, 2),
        "C": (2, 2),
        "S1": (-2, 1),
        "S2": (2, 1),
        "D": (0, 0),
        "S": (0, -1),
    }

    plt.figure(figsize=(7, 7))
    nx.draw_networkx_nodes(G, pos, node_size=1600, node_color="lightgrey")
    nx.draw_networkx_labels(G, pos, font_size=10)

    if flow:
        widths = [1 + 0.08 * flow.get(u, {}).get(v, 0) for u, v in G.edges()]
    else:
        widths = 1.5

    nx.draw_networkx_edges(G, pos, arrows=True, width=widths)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, "capacity"),
        font_size=8
    )

    plt.title(title)
    plt.axis("off")

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches="tight")

    plt.show()


# =========================
# Main
# =========================

def main():
    parser = argparse.ArgumentParser(description="Evacuation optimization with figures")
    parser.add_argument("--alpha", type=float, default=6.0, help="Stairs penalty")
    parser.add_argument("--speed", type=float, default=1.2, help="Walking speed (m/s)")
    args = parser.parse_args()

    # -------- Baseline --------
    G = build_graph(args.alpha, args.speed)

    draw_graph(G, title="Figure 1: Building network with corridor capacities", filename="figure_1.png")

    max_flow, _ = compute_max_flow(G)
    cost, flow = min_cost_for_flow(G, max_flow)

    print("=== BASELINE ===")
    print(f"Max evacuated flow (people/min): {max_flow}")
    print(f"Min-cost for that flow (scaled x10): {cost}")
    print_positive_flows(flow)

    draw_graph(G, flow, title="Figure 2: Optimal evacuation flows (baseline)", filename="figure_2.png")

    # -------- Scenario: A -> B closed --------
    G2 = G.copy()
    if G2.has_edge("A", "B"):
        G2.remove_edge("A", "B")

    max_flow2, _ = compute_max_flow(G2)
    cost2, flow2 = min_cost_for_flow(G2, max_flow2)

    print("\n=== SCENARIO: A → B CLOSED ===")
    print(f"Max evacuated flow (people/min): {max_flow2}")
    print(f"Min-cost for that flow (scaled x10): {cost2}")
    print_positive_flows(flow2)

    draw_graph(
        G2,
        flow2,
        title="Figure 3: Evacuation flows after closing corridor A→B",
        filename="figure_3.png"
    )


if __name__ == "__main__":
    main()
