# Pedestrian Flow Optimization in a University Building during Emergency Evacuation

**Authors:** Anaïs Berkowicz—Bach, Clémence Morin

## Project description
This project studies the evacuation of a university building during a fire emergency using an Operations Research approach.
The building is modeled as a directed network where nodes represent areas of the building and edges represent corridors with limited capacity.

The objective is to maximize the number of evacuated occupants while minimizing the total evacuation time.

## Mathematical model
The evacuation problem is formulated as a network flow optimization problem.
A two-step approach is used:
1. Maximization of the total evacuation flow (maximum flow).
2. Minimization of the total evacuation time among all maximum-flow solutions (minimum-cost flow).

Corridor capacities, travel times, and penalties for stairs are included in the model.
Elevators are excluded in accordance with fire safety regulations.

## Code structure
- `code/main_nofig.py`: computes the optimal evacuation flow for the baseline scenario and for a disruption scenario where corridor A→B is closed.
- `code/figures.py`: generates the figures used in the report.

## Figures
- `figure1.png`: network representation of the building with corridor capacities.
- `figure2.png`: optimal evacuation flows under baseline conditions.
- `figure3.png`: optimal evacuation flows after closing corridor A→B.

## How to run the code
Install the required Python libraries:
```bash
pip install networkx matplotlib
