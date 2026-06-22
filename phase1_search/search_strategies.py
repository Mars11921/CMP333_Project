from __future__ import annotations

from phase1_search.search_problem import DeliveryPlan, SearchAlgorithm, SearchProblem, SearchResult
from simulator.campus_map import CampusMap
from simulator.models import Delivery, Position

def plan_delivery_route(
    campus_map: CampusMap,
    start: Position,
    deliveries: list[Delivery],
    search_algorithm: SearchAlgorithm,
) -> DeliveryPlan:
    """Plan a route that picks up and delivers all given deliveries in order."""
    raise NotImplementedError("Phase 1 TODO: implement delivery route planning.")

def uniform_cost_search(problem: SearchProblem) -> SearchResult:
    """Return the lowest-cost path from start to goal using UCS."""
    raise NotImplementedError("Phase 1 TODO: implement uniform cost search.")


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

