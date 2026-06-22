from __future__ import annotations

import json
from pathlib import Path

from simulator.campus_map import CampusMap
from simulator.models import Action, Delivery, DeliveryScenario, Position, RobotState


MOVE_DELTAS = {
    Action.UP: (0, -1),
    Action.DOWN: (0, 1),
    Action.LEFT: (-1, 0),
    Action.RIGHT: (1, 0),
    Action.WAIT: (0, 0),
}


class CampusEnvironment:
    def __init__(
        self,
        campus_map: CampusMap,
        deliveries: list[Delivery],
        initial_state: Position,
    ) -> None:
        self.campus_map = campus_map
        self.deliveries = deliveries
        self.step_count = 0
        self.robot = RobotState(
            robot_id="R1",
            position=initial_state,
            color=(36, 99, 235),
        )
        self.events: list[str] = ["Demo started."]

    def step(self, action: Action) -> None:
        if action == Action.PICKUP:
            self.pickup()
            self.step_count += 1
            return
        if action == Action.DELIVER:
            self.deliver()
            self.step_count += 1
            return

        dx, dy = MOVE_DELTAS[action]
        next_position = Position(self.robot.position.x + dx, self.robot.position.y + dy)

        if self.campus_map.is_walkable(next_position):
            self.robot.position = next_position
            self.robot.total_cost += 1 if action != Action.WAIT else 0
            self.events.append(f"Step {self.step_count}: R1 used {action.value}.")
        else:
            self.events.append(f"Step {self.step_count}: R1 hit a wall using {action.value}.")

        self.step_count += 1

    def pickup(self) -> None:
        if self.robot.carrying_delivery_id is not None:
            self.events.append(
                f"Step {self.step_count}: R1 cannot pick up while carrying "
                f"{self.robot.carrying_delivery_id}."
            )
            return

        for delivery in self.deliveries:
            if delivery.pickup == self.robot.position:
                self.robot.carrying_delivery_id = delivery.delivery_id
                self.events.append(f"Step {self.step_count}: R1 picked up {delivery.delivery_id}.")
                return

        self.events.append(f"Step {self.step_count}: R1 tried to pick up, but no package is here.")

    def deliver(self) -> None:
        if self.robot.carrying_delivery_id is None:
            self.events.append(f"Step {self.step_count}: R1 tried to deliver without a package.")
            return

        for delivery in self.deliveries:
            if (
                delivery.delivery_id == self.robot.carrying_delivery_id
                and delivery.dropoff == self.robot.position
            ):
                self.robot.completed_delivery_ids.append(delivery.delivery_id)
                self.events.append(f"Step {self.step_count}: R1 delivered {delivery.delivery_id}.")
                self.robot.carrying_delivery_id = None
                return

        self.events.append(
            f"Step {self.step_count}: R1 is not at the dropoff for "
            f"{self.robot.carrying_delivery_id}."
        )


def load_delivery_scenario(path: str | Path) -> DeliveryScenario:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, list):
        raise ValueError(
            "Delivery files must contain an object with 'initial_state' and 'deliveries'."
        )

    raw_deliveries = raw["deliveries"]
    deliveries: list[Delivery] = []

    for item in raw_deliveries:
        deliveries.append(
            Delivery(
                delivery_id=item["id"],
                pickup=Position(*item["pickup"]),
                dropoff=Position(*item["dropoff"]),
                reward=int(item["reward"]),
            )
        )

    return DeliveryScenario(
        initial_state=Position(*raw["initial_state"]),
        deliveries=deliveries,
    )


def load_deliveries(path: str | Path) -> list[Delivery]:
    return load_delivery_scenario(path).deliveries
