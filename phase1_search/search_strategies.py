from __future__ import annotations

import heapq

from phase1_search.search_problem import DeliveryPlan, SearchAlgorithm, SearchProblem, SearchResult, actions_from_path
from simulator.campus_map import CampusMap
from simulator.models import Action, Delivery, Position

def plan_delivery_route(
    campus_map: CampusMap,
    start: Position,
    deliveries: list[Delivery],
    search_algorithm: SearchAlgorithm,
) -> DeliveryPlan:
    """Plan a route that picks up and delivers all given deliveries in order."""
    for delivery in deliveries:
        # step 1: walk to the pickup
        problem = SearchProblem(campus_map, current, delivery.pickup)
        result = search_algorithm(problem)
        all_actions += result.actions
        total_cost += result.cost
        total_nodes += result.nodes_expanded
        current = delivery.pickup

        # step 2: PICKUP
        carrying = pickup(current, delivery, carrying)
        all_actions.append(Action.PICKUP)

        # step 3: walk to the dropoff  (step 1 again, target = dropoff)
        problem = SearchProblem(campus_map, current, delivery.dropoff)
        result = search_algorithm(problem)
        all_actions += result.actions
        total_cost += result.cost
        total_nodes += result.nodes_expanded
        current = delivery.dropoff

        # step 4: DELIVER  (step 2 again, but putting down)
        deliver(current, delivery, carrying)
        carrying = None
        all_actions.append(Action.DELIVER)
        completed.append(delivery.delivery_id)

def uniform_cost_search(problem: SearchProblem) -> SearchResult: # Will Implement This First F(n) = G(n) => Evaluation Function
    """Return the lowest-cost path from start to goal using UCS."""
    start = problem.initial_state # Store State Node In Start

    frontier = [] # Intially The Frontier Is Empty
    counter = 0
    
    heapq.heappush(frontier, (0, 0, start)) # We Push Start Node Along With Its Cost i.e. (0) & Counter In Case Of Tie Between Nodes
    counter += 1 # Increment Counter After Pushing Initial Node

    came_from = {start: None} # Dictionary That Stores Node & Its Parent
    cost_so_far = {start: 0} # Dictionary That Stores Cost So Far From Current Node
    expanded = set() # A Set Of Explored Nodes, Initially Empty
    nodes_expanded = 0 # Variable Stores Number Of Nodes Expanded, Initially Zero

    while frontier:

        if current in expanded:
            continue
        expanded.add(current)
        nodes_expanded += 1

        if problem.is_goal(current):
            break

        for action in problem.actions(current):
            next_pos = problem.result(current, action)
            new_cost = cost + problem.cost(current, action, next_pos)

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                came_from[next_pos] = current
                heapq.heappush(frontier, (new_cost, counter, next_pos))
                counter += 1
    path = []
    node = problem.goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()

    return SearchResult(
        path=path,
        actions=actions_from_path(path),
        cost=cost_so_far[problem.goal],
        nodes_expanded=nodes_expanded,
    )

def greedy_best_first_search(problem: SearchProblem) -> SearchResult:
    """Return a path from start to goal using greedy best-first search."""
    raise NotImplementedError("Phase 1 TODO: implement greedy best-first search.")


def a_star_search(problem: SearchProblem) -> SearchResult:
    """Return the lowest-cost path from start to goal using A* search."""
    raise NotImplementedError("Phase 1 TODO: implement A* search.")


def pickup(position: Position, delivery: Delivery, carrying_delivery_id: str | None) -> str:
    """Pick up a delivery if the robot is at the correct pickup location."""
    if carrying_delivery_id is not None:
        raise ValueError(f"Cannot pick up {delivery.delivery_id}; already carrying {carrying_delivery_id}.")
    if position != delivery.pickup:
        raise ValueError(f"Cannot pick up {delivery.delivery_id} from {position}; pickup is {delivery.pickup}.")
    return delivery.delivery_id


def deliver(position: Position, delivery: Delivery, carrying_delivery_id: str | None) -> None:
    """Deliver a package if the robot is at the correct dropoff location."""
    if carrying_delivery_id != delivery.delivery_id:
        raise ValueError(f"Cannot deliver {delivery.delivery_id}; carrying {carrying_delivery_id}.")
    if position != delivery.dropoff:
        raise ValueError(f"Cannot deliver {delivery.delivery_id} from {position}; dropoff is {delivery.dropoff}.")
    return None

