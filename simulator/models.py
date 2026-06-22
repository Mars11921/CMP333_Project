from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class Position:
    x: int
    y: int


class Action(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    WAIT = "WAIT"
    PICKUP = "PICKUP"
    DELIVER = "DELIVER"


@dataclass(frozen=True)
class Delivery:
    delivery_id: str
    pickup: Position
    dropoff: Position
    reward: int


@dataclass(frozen=True)
class DeliveryScenario:
    initial_state: Position
    deliveries: list[Delivery]


@dataclass
class RobotState:
    robot_id: str
    position: Position
    color: tuple[int, int, int]
    total_cost: int = 0
    carrying_delivery_id: str | None = None
    completed_delivery_ids: list[str] = field(default_factory=list)
