# Phase 1: Search Strategies

In this phase, each team implements pickup-and-delivery route planning for the campus robot.

The robot is given:

- a campus map
- a start location
- one or more deliveries

The route should handle all deliveries in the order they appear in the delivery file:

```text
initial_state -> P1 -> D1 -> P2 -> D2 -> ...
```

## Search Problem

`search_problem.py` implements the search problem as follows:

```text

initial_state:
the robot's current position represented as (x, y)

is_goal(state):
current position == target position

actions(state):
UP, DOWN, LEFT, RIGHT

result(state, action):
move to the neighboring cell if it is walkable

cost(state, action, next_state):
1 per move
```

Use `manhattan_distance` for heuristic in A*

## Algorithms to Implement

Students must implement the following functions in `search_strategies.py`:

- `uniform_cost_search`
- `greedy_best_first_search`
- `a_star_search`
- `plan_delivery_route`

The `pickup(...)` and `deliver(...)` helper functions are already provided. Use them inside `plan_delivery_route(...)`; do not rewrite them.

## Delivery Route Planning

For each delivery, the route planner should:

```text
search from current position to pickup
PICKUP
search from pickup to dropoff
DELIVER
```

For multiple deliveries, continue from the previous dropoff:

```text
search from initial_state to P1
PICKUP
search from P1 to D1
DELIVER
search from D1 to P2
PICKUP
search from P2 to D2
DELIVER
```

The route should return a `DeliveryPlan` containing the complete action list, total movement cost, total nodes expanded, and completed delivery IDs.

## Run Phase 1 Check

From the project folder:

```bash
cd campus_robot
python phase1_search/check_phase1.py
```

The check will fail until the search algorithms and delivery route planner are implemented.

## Run Visual Demo

```bash
cd campus_robot
python run_phase1_demo.py --source student --algorithm astar
```

Available algorithm names:

```text
ucs
greedy
astar
```

The default scenario is `public`.

```bash
cd campus_robot
python run_phase1_demo.py --source student --algorithm astar --scenario public
```

## Map Symbols

```text
# = wall or blocked cell
. = walkable path
```

The `.txt` map files only encode walls and corridors. Initial robot locations, pickups, and dropoffs live in JSON scenario/delivery files.

Public Phase 1 delivery file format:

```json
{
  "initial_state": [1, 1],
  "deliveries": [
    {
      "id": "delivery_1",
      "pickup": [9, 3],
      "dropoff": [10, 8],
      "reward": 100
    },
    {
      "id": "delivery_2",
      "pickup": [10, 2],
      "dropoff": [7, 3],
      "reward": 100
    }
  ]
}
```

The `deliveries` list may contain one or more deliveries. The route planner should handle them in the order they appear in the list.

The Pygame viewer labels deliveries by delivery order:

```text
P1 -> D1
P2 -> D2
```

The numbered labels are drawn from `data/deliveries.json`.

The simulation logic is separate from the Pygame drawing code:

- `simulator/environment.py` controls the world state and movement rules.
- `visualization/pygame_viewer.py` only draws the current world state.
- `phase1_search/search_problem.py` defines the point-to-point search problem.
- `phase1_search/search_strategies.py` is the only file students should edit for Phase 1.

## Phase 1 Student Task

Students should edit only:

```text
phase1_search/search_strategies.py
```

The `pickup(...)` and `deliver(...)` helper functions are already provided. Students implement:

```text
uniform_cost_search
greedy_best_first_search
a_star_search
plan_delivery_route
```

The full delivery route should look like:

```text
move from initial_state to P1
PICKUP
move from P1 to D1
DELIVER
move from D1 to P2
PICKUP
move from P2 to D2
DELIVER
...
```
