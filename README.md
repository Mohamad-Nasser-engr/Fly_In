# *This project has been created as part of the 42 curriculum by [monasser](https://profile-v3.intra.42.fr/users/monasser).*

# Description

The **Fly_In** project simulates and visualizes a multi-drone navigation system in a grid-based environment. The main goal is to route multiple drones from a starting zone to a destination while respecting zone types (Normal, Restricted, Priority, Blocked), zone capacities, and link constraints. The system minimizes the total number of turns required for all drones to reach the destination.

## Key features:

- Drones prioritize reaching the end efficiently using a Reverse Dijkstra pathfinding algorithm.
- Supports multiple zone types with different movement costs and restrictions.
- Handles link capacities between zones to avoid overcrowding.
- Provides a visual representation using the Arcade library with smooth animations.

## Instructions
### Requirements
- Python 3.11+
- arcade library
- Standard Python libraries (heapq, copy, sys, math, enum)

### Installation
```bash
make install
```

### Run the main script with the input map file:
```bash
python3 -m main <map_file>
```
or
```bash
make run
```

The simulation will display a window showing drones moving through the network, updating turn by turn.

## Algorithm & Implementation Strategy
### Input Parsing:
- Reads the map and prepares zones, links, and drone counts.
- Validates metadata and constraints
### Pathfinding:
ReverseDijkstra computes the distance from each zone to the end using a reverse Dijkstra algorithm. Each zone’s type affects its movement cost:
- Priority: 0.9
- Normal: 1
- Restricted: 2
- Blocked: ∞ (inaccessible)
### Simulation:
#### Simulation manages turn-by-turn drone movements:
- Drones move along the optimal path to the end.
- Movement respects zone capacities, link capacities, and transit states.
- Restricted zones and links are handled carefully to avoid congestion.
#### Turn Handling:
Each turn is simulated with simulate_turn(), updating drone locations, transit states, and link usage.
### Visualization:
- Window uses Arcade to render zones, links, and drones with smooth animations, including:
- Drone counts per zone
- Color-coded zones (including rainbow and custom colors)
Animated transitions between nodes

This combination ensures efficient and visually clear simulation.

### Visual Representation

The display shows:

- Zones as circles, colored based on type or custom value.
- Drones as small moving circles with IDs.
- Links between zones as gray lines.
- Dynamic drone counts and movement animations for each turn.

### Visual features enhance user experience by:

- Allowing real-time tracking of each drone.
- Clearly showing congestion and routing choices.
- Supporting color-coded priority zones for easier interpretation.

### AI Usage

Gemini was used throughout this project for:
- Debugging errors in the code and identifying issues with logic or input handling.
- Researching algorithms to determine the most efficient pathfinding strategy (Reverse Dijkstra) for the drones.
- Assisting with the display and visualization logic using the Arcade library, including smooth animations and dynamic drone tracking.
- Drafing the README.

### Resources
- Arcade library: https://arcade.academy/
- Dijkstra’s algorithm reference: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm