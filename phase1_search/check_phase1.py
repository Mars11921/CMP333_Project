from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from phase1_search.search_strategies import (
    a_star_search,
    plan_delivery_route,
    greedy_best_first_search,
    uniform_cost_search,
)
from phase1_search.search_problem import SearchProblem
from simulator.campus_map import load_campus_map
from simulator.environment import load_delivery_scenario
from simulator.models import Action, Delivery, Position


def validate_plan(name: str, campus_map, initial_state: Position, plan, deliveries: list[Delivery]) -> None:
    if not plan.actions:
        raise AssertionError(f"{name} returned an empty delivery plan.")
    if plan.cost < 0:
        raise AssertionError(f"{name} returned a negative path cost.")
    if plan.nodes_expanded <= 0:
        raise AssertionError(f"{name} must report nodes_expanded.")

    state = initial_state
    carrying_delivery_id: str | None = None
    completed_delivery_ids: list[str] = []
    delivery_index = 0
    replay_cost = 0

    for action in plan.actions:
        if action == Action.PICKUP:
            if delivery_index >= len(deliveries):
                raise AssertionError(f"{name} picked up after all deliveries were complete.")
            delivery = deliveries[delivery_index]
            if carrying_delivery_id is not None:
                raise AssertionError(f"{name} picked up while already carrying a package.")
            if state != delivery.pickup:
                raise AssertionError(f"{name} picked up at {state}, not {delivery.pickup}.")
            carrying_delivery_id = delivery.delivery_id
        elif action == Action.DELIVER:
            if delivery_index >= len(deliveries):
                raise AssertionError(f"{name} delivered after all deliveries were complete.")
            delivery = deliveries[delivery_index]
            if carrying_delivery_id != delivery.delivery_id:
                raise AssertionError(f"{name} delivered without carrying {delivery.delivery_id}.")
            if state != delivery.dropoff:
                raise AssertionError(f"{name} delivered at {state}, not {delivery.dropoff}.")
            completed_delivery_ids.append(delivery.delivery_id)
            carrying_delivery_id = None
            delivery_index += 1
        else:
            movement_problem = SearchProblem(campus_map, state, state)
            next_state = movement_problem.result(state, action)
            replay_cost += movement_problem.cost(state, action, next_state)
            state = next_state

    expected_completed_ids = [delivery.delivery_id for delivery in deliveries]
    if carrying_delivery_id is not None:
        raise AssertionError(f"{name} ended while still carrying a package.")
    if completed_delivery_ids != expected_completed_ids:
        raise AssertionError(
            f"{name} completed {completed_delivery_ids}, expected {expected_completed_ids}."
        )
    if plan.completed_delivery_ids != expected_completed_ids:
        raise AssertionError(
            f"{name} reported completed deliveries {plan.completed_delivery_ids}, "
            f"expected {expected_completed_ids}."
        )
    if deliveries and state != deliveries[-1].dropoff:
        raise AssertionError(f"{name} ended at {state}, not final dropoff {deliveries[-1].dropoff}.")
    if plan.cost != replay_cost:
        raise AssertionError(f"{name} reported cost {plan.cost}, but replay cost is {replay_cost}.")


def main() -> int:
    campus_map = load_campus_map(PROJECT_ROOT / "data" / "campus_map.txt")
    scenario = load_delivery_scenario(PROJECT_ROOT / "data" / "deliveries.json")

    algorithms = {
        "UCS": uniform_cost_search,
        "Greedy": greedy_best_first_search,
        "A*": a_star_search,
    }

    failed = False
    for name, algorithm in algorithms.items():
        try:
            plan = plan_delivery_route(campus_map, scenario.initial_state, scenario.deliveries, algorithm)
            validate_plan(name, campus_map, scenario.initial_state, plan, scenario.deliveries)
        except NotImplementedError as exc:
            failed = True
            print(f"{name}: NOT IMPLEMENTED - {exc}")
        except Exception as exc:
            failed = True
            print(f"{name}: FAILED - {exc}")
        else:
            print(
                f"{name}: PASS "
                f"cost={plan.cost} "
                f"actions={len(plan.actions)} "
                f"expanded={plan.nodes_expanded}"
            )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
