from __future__ import annotations

import argparse
from pathlib import Path

from simulator.campus_map import load_campus_map
from simulator.environment import CampusEnvironment, load_delivery_scenario
from simulator.models import Action
from visualization.pygame_viewer import PygameViewer


ROOT = Path(__file__).resolve().parent


SCRIPTED_ROUTE = [
    Action.RIGHT,
    Action.RIGHT,
    Action.RIGHT,
    Action.DOWN,
    Action.DOWN,
    Action.DOWN,
    Action.LEFT,
    Action.LEFT,
    Action.LEFT,
    Action.DOWN,
    Action.DOWN,
    Action.RIGHT,
    Action.RIGHT,
    Action.RIGHT,
    Action.RIGHT,
    Action.RIGHT,
    Action.RIGHT,
    Action.RIGHT,
    Action.RIGHT,
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Pygame campus robot visual demo.")
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Stop after this many frames. Useful for automated smoke tests.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    campus_map = load_campus_map(ROOT / "data" / "campus_map.txt")
    scenario = load_delivery_scenario(ROOT / "data" / "deliveries.json")
    environment = CampusEnvironment(campus_map, scenario.deliveries, scenario.initial_state)
    viewer = PygameViewer(environment)

    route_index = 0
    frames_between_steps = 18
    frame_count = 0
    running = True

    while running:
        if viewer.handle_quit():
            running = False

        if route_index < len(SCRIPTED_ROUTE) and frame_count % frames_between_steps == 0:
            environment.step(SCRIPTED_ROUTE[route_index])
            route_index += 1

        viewer.draw()
        viewer.tick()
        frame_count += 1
        if args.max_frames is not None and frame_count >= args.max_frames:
            running = False

    viewer.close()


if __name__ == "__main__":
    main()
