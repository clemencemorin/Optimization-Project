import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

edges = [
    ("N", "A", 120),
    ("A", "B", 60),
    ("A", "C", 60),
    ("B", "S1", 40),
    ("C", "S2", 40),
    ("S1", "D", 40),
    ("S2", "D", 40),
    ("D", "S", 120),
    ("B", "C", 20),
    ("C", "B", 20),
    ("S1", "S2", 15),
    ("S2", "S1", 15),
]

for u, v, cap in edges:
    G.add_edge(u, v, capacity=cap)


pos = {
    "N": (0, 4),
    "A": (0, 3),
    "B": (-1.5, 2),
    "C": (1.5, 2),
    "S1": (-1.5, 1),
    "S2": (1.5, 1),
    "D": (0, 0),
    "S": (0, -1),
}

plt.figure(figsize=(7, 7))

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1600,
    node_color="lightgrey",
    font_size=10,
    arrows=True,
    edge_color="black"
)

capacities = nx.get_edge_attributes(G, "capacity")
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=capacities,
    font_size=8
)

plt.title("Figure 1: Directed graph of the university building with corridor capacities")
plt.axis("off")
plt.tight_layout()
plt.show()
flow_value, flow_dict = nx.maximum_flow(G, "N", "S")
edge_widths = []
for u, v in G.edges():
    f = flow_dict[u][v]
    edge_widths.append(1 + 0.08 * f) 

plt.figure(figsize=(7, 7))


nx.draw_networkx_nodes(
    G,
    pos,
    node_size=1600,
    node_color="lightgrey"
)


nx.draw_networkx_edges(
    G,
    pos,
    width=edge_widths,
    edge_color="black",
    arrows=True
)


nx.draw_networkx_labels(
    G,
    pos,
    font_size=10
)

capacities = nx.get_edge_attributes(G, "capacity")
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=capacities,
    font_size=8
)

plt.title("Figure 2: Optimal evacuation flows under baseline conditions")
plt.axis("off")
plt.tight_layout()
plt.show()

import networkx as nx
import matplotlib.pyplot as plt

G3 = G.copy()
if G3.has_edge("A", "B"):
    G3.remove_edge("A", "B")


flow_value3, flow_dict3 = nx.maximum_flow(G3, "N", "S")


edge_widths3 = []
for u, v in G3.edges():
    f = flow_dict3[u][v]
    edge_widths3.append(1 + 0.08 * f)  # same scaling as Figure 


plt.figure(figsize=(7, 7))


nx.draw_networkx_nodes(
    G3,
    pos,
    node_size=1600,
    node_color="lightgrey"
)


nx.draw_networkx_edges(
    G3,
    pos,
    width=edge_widths3,
    edge_color="black",
    arrows=True
)


nx.draw_networkx_labels(G3, pos, font_size=10)


capacities3 = nx.get_edge_attributes(G3, "capacity")
nx.draw_networkx_edge_labels(
    G3,
    pos,
    edge_labels=capacities3,
    font_size=8
)

plt.title("Figure 3: Optimal evacuation flows after closing corridor A → B")
plt.axis("off")
plt.tight_layout()
plt.show()

print("Scenario A→B closed: max flow =", flow_value3)
