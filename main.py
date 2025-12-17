#!/usr/bin/env python3
"""
Pedestrian Flow Optimization in a University Building during Emergency Evacuation
Authors: Anaïs Berkowicz—Bach, Clémence Morin

MAIN SCRIPT (NO FIGURES)

This script builds the evacuation network and computes:
  1) Maximum evacuated flow from N (Entrance) to S (Exit) using capacities
  2) A minimum-cost flow among all solutions that achieve that maximum flow
  3) The same metrics for the disruption scenario where corridor A->B is closed

It does NOT generate any figures (you already have a separate script for that).

Requirements:
  pip install networkx
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, Tuple

import networkx as nx


@dataclass(frozen=True)
class EdgeSpec:
    u: str
    v: str
    capacity: int
    length: float
    kind: str  # "corridor", "ramp", "stairs" (elevator excluded)


def default_edges() -> list[EdgeSpec]:
    """
    Baseline network edges.

    Note: Lengths are plausible placeholders (relative units).
    Replace them with real corridor lengths if you have them.
    """
    def L(kind: str) -> float:
        return {"corridor": 12.0, "ramp": 14.0, "stairs": 10.0}[kind]

    return [
        EdgeSpec("N", "A", 120, L("corridor"), "corridor"),
        EdgeSpec("A", "B", 60,  L("corridor"), "corridor"),
        EdgeSpec("A", "C", 60,  L("corridor"), "corridor"),
        EdgeSpec("B", "S1", 40, L("corridor"), "corridor"),
        EdgeSpec("C", "S2", 40, L("corridor"), "corridor"),
        # Encode preference: stairs are penalized in cost
        EdgeSpec("S1", "D", 40, L("stairs"), "stairs"),
        EdgeSpec("S2", "D", 40, L("stairs"), "stairs"),
        EdgeSpec("D", "S", 120, L("corridor"), "corridor"),
        # Crosslinks
        EdgeSpec("B", "C", 20, 8.0, "corridor"),
        EdgeSpec("C", "B", 20, 8.0, "corridor"),
        EdgeSpec("S1", "S2", 15, 6.0, "corridor"),
        EdgeSpec("S2", "S1", 15, 6.0, "corridor"),
    ]


def build_graph(alpha_stairs: float = 6.0, v: float = 1.2) -> nx.DiGraph:
    """
    Build a directed graph with:
      - capacity: people/min
      - weight: integer cost used by NetworkX min_cost_flow

    Travel time model (report):
        T_ij = L_ij / v + gamma_ij
    where gamma_ij = 0 for ramps/corridors, and alpha_stairs for stairs.
    """
    G = nx.DiGraph()

    for e in default_edges():
        gamma = alpha_stairs if e.kind == "stairs" else 0.0
        Tij = e.length / v + gamma

        # min_cost_flow expects integer costs; scale by 10 for one decimal precision
        cost_int = int(round(Tij * 10))

        G.add_edge(
            e.u, e.v,
            capacity=int(e.capacity),
            length=float(e.length),
            kind=e.kind,
            gamma=float(gamma),
            Tij=float(Tij),
            weight=int(cost_int),
        )

    return G


def compute_max_flow(G: nx.DiGraph, source: str = "N", sink: str = "S") -> Tuple[int, Dict]:
    """Maximum flow with capacities only."""
    flow_value, flow_dict = nx.maximum_flow(G, source, sink, capacity="capacity")
    return int(flow_value), flow_dict


def min_cost_for_flow(G: nx.DiGraph, flow_amount: int, source: str = "N", sink: str = "S") -> Tuple[int, Dict]:
    """
    Minimum-cost flow that sends exactly `flow_amount` from source to sink.
    Implemented via node demands.
    """
    H = G.copy()

    for n in H.nodes():
        H.nodes[n]["demand"] = 0
    H.nodes[source]["demand"] = -int(flow_amount)
    H.nodes[sink]["demand"] = int(flow_amount)

    flow_dict = nx.min_cost_flow(H, demand="demand", capacity="capacity", weight="weight")

    total_cost = 0
    for u, nbrs in flow_dict.items():
        for v, f in nbrs.items():
            if f:
                total_cost += int(f) * int(H[u][v]["weight"])

    return int(total_cost), flow_dict


def print_positive_flows(flow_dict: Dict) -> None:
    """Print only edges with positive flow."""
    for u, nbrs in flow_dict.items():
        for v, f in nbrs.items():
            if f:
                print(f"  {u} -> {v}: {f}")


def run_case(G: nx.DiGraph, label: str) -> None:
    """Run max-flow then min-cost among max-flow solutions."""
    max_flow_val, _ = compute_max_flow(G, "N", "S")
    min_cost, flow = min_cost_for_flow(G, max_flow_val, "N", "S")

    print(f"=== {label} ===")
    print(f"Max evacuated flow (people/min): {max_flow_val}")
    print(f"Min-cost for that flow (cost scaled by x10): {min_cost}")
    print("Positive flows:")
    print_positive_flows(flow)
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Evacuation optimization (no figures).")
    parser.add_argument("--alpha", type=float, default=6.0, help="Stairs penalty alpha (time units).")
    parser.add_argument("--speed", type=float, default=1.2, help="Average walking speed v.")
    args = parser.parse_args()

    # Baseline
    G = build_graph(alpha_stairs=args.alpha, v=args.speed)
    run_case(G, "BASELINE")

    # Scenario: close corridor A->B
    G_scen = G.copy()
    if G_scen.has_edge("A", "B"):
        G_scen.remove_edge("A", "B")
    run_case(G_scen, "SCENARIO: A->B CLOSED")


if __name__ == "__main__":
    main()
