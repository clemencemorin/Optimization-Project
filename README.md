# Pedestrian Flow Optimization in a University Building during Emergency Evacuation

**Authors:** Anaïs Berkowicz—Bach, Clémence Morin

---

## Project description

This project analyzes the evacuation of a university building during a fire emergency using an **Operations Research** approach.

The building is modeled as a **directed network**:
- **Nodes** represent key areas of the building,
- **Edges** represent corridors, stairs, or ramps with **limited evacuation capacities**.

The goal is to determine how occupants should be routed through the building in order to:
1. **Maximize the number of people evacuated per unit of time**, and
2. **Minimize the total evacuation time** for those occupants.

---

## Mathematical model

The evacuation problem is formulated as a **network flow optimization problem** solved in two successive steps:

1. **Maximum Flow Problem**  
   Determines the maximum number of occupants (people per minute) that can be evacuated from the entrance node **N** to the exit node **S**, subject to corridor capacity constraints.

2. **Minimum-Cost Flow Problem**  
   Among all feasible solutions achieving this maximum flow, the model selects the one that **minimizes total evacuation time**.

### Travel time model

For each edge \( (i, j) \), the travel time is defined as:

\[
T_{ij} = \frac{L_{ij}}{v} + \gamma_{ij}
\]

where:
- \( L_{ij} \) is the corridor length,
- \( v \) is the average walking speed,
- \( \gamma_{ij} \) is a penalty term applied to stairs.

Elevators are excluded from the model in accordance with fire safety regulations.

---

## Scenarios analyzed

The code evaluates two scenarios:

- **Baseline scenario**: all corridors are available.
- **Disruption scenario**: corridor **A → B** is closed, simulating a blocked passage due to fire or smoke.

For each scenario, the maximum evacuation flow and the corresponding minimum-cost flow are computed and visualized.

---

## Code structure

The project relies on a **single Python script**:

- `main.py`  
  - Builds the evacuation network  
  - Computes the maximum evacuation flow  
  - Computes the minimum-cost flow among maximum-flow solutions  
  - Generates all figures used in the report  
  - Prints numerical results to the console  

---

## Figures generated

Running the script produces the following figures:

- `figure_1.png`: network representation of the building with corridor capacities.
- `figure_2.png`: optimal evacuation flows for the baseline scenario.
- `figure_3.png`: optimal evacuation flows after closing corridor **A → B**.

In flow figures, edge thickness is proportional to the number of evacuees using each corridor.

---

## How to run the code

### Requirements

Install the required Python libraries:
```bash
pip install networkx matplotlib
