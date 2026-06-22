from __future__ import annotations

import argparse
import importlib
from pathlib import Path

from simulator.campus_map import CampusMap, load_campus_map
from simulator.environment import CampusEnvironment, load_delivery_scenario
from simulator.models import Delivery, Position
from visualization.pygame_viewer import PygameViewer


ROOT = Path(__file__).resolve().parent

SOURCE_MODULES = {
    "student": "phase1_search.search_strategies",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize a Phase 1 search route.")
    parser.add_argument(
        "--source",
        choices=sorted(SOURCE_MODULES),
        default="student",
        help="Use the student Phase 1 implementation.",
    )
    parser.add_argument(
        "--algorithm",
        choices=("ucs", "greedy", "astar"),
        default="astar",
        help="Search algorithm to visualize.",
    )
    parser.add_argument(
        "--scenario",
        choices=("public",),
        default="public",
        help="Scenario to visualize.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Stop after this many frames. Useful for automated smoke tests.",
    )
    return parser.parse_args()


def load_algorithm(source: str, algorithm: str):
    module = importlib.import_module(SOURCE_MODULES[source])
    function_names = {
        "ucs": "uniform_cost_search",
        "greedy": "greedy_best_first_search",
        "astar": "a_star_search",
    }
    return getattr(module, function_names[algorithm])


def load_route_planner(source: str):
    module = importlib.import_module(SOURCE_MODULES[source])
    return getattr(module, "plan_delivery_route")


def load_problem_and_deliveries(scenario_name: str) -> tuple[Position, CampusMap, list[Delivery]]:
    campus_map = load_campus_map(ROOT / "data" / "campus_map.txt")
    scenario = load_delivery_scenario(ROOT / "data" / "deliveries.json")
    return scenario.initial_state, campus_map, scenario.deliveries


def main() -> int:
    args = parse_args()
    start, campus_map, deliveries = load_problem_and_deliveries(args.scenario)
    algorithm = load_algorithm(args.source, args.algorithm)
    plan_delivery_route = load_route_planner(args.source)

    try:
        result = plan_delivery_route(campus_map, start, deliveries, algorithm)
    except (NotImplementedError, ValueError) as exc:
        print(exc)
        return 1

    print(
        f"{args.source}/{args.algorithm}/{args.scenario}: "
        f"cost={result.cost}, "
        f"actions={len(result.actions)}, "
        f"expanded={result.nodes_expanded}"
    )

    environment = CampusEnvironment(campus_map, deliveries, start)
    viewer = PygameViewer(environment)

    action_index = 0
    frames_between_steps = 18
    frame_count = 0
    running = True

    while running:
        if viewer.handle_quit():
            running = False

        if action_index < len(result.actions) and frame_count % frames_between_steps == 0:
            environment.step(result.actions[action_index])
            action_index += 1

        viewer.draw()
        viewer.tick()
        frame_count += 1
        if args.max_frames is not None and frame_count >= args.max_frames:
            running = False

    viewer.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
