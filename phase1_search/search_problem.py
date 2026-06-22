from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from simulator.campus_map import CampusMap
from simulator.models import Action, Position


MOVE_ACTIONS = (Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT)

ACTION_DELTAS = {
    Action.UP: (0, -1),
    Action.DOWN: (0, 1),
    Action.LEFT: (-1, 0),
    Action.RIGHT: (1, 0),
}


@dataclass(frozen=True)
class SearchProblem:
    campus_map: CampusMap
    initial_state: Position
    goal: Position

    def is_goal(self, position: Position) -> bool:
        return position == self.goal

    def actions(self, state: Position) -> list[Action]:
        valid_actions: list[Action] = []
        for action in MOVE_ACTIONS:
            dx, dy = ACTION_DELTAS[action]
            next_position = Position(state.x + dx, state.y + dy)
            if self.campus_map.is_walkable(next_position):
                valid_actions.append(action)
        return valid_actions

    def result(self, state: Position, action: Action) -> Position:
        dx, dy = ACTION_DELTAS[action]
        next_position = Position(state.x + dx, state.y + dy)
        if not self.campus_map.is_walkable(next_position):
            raise ValueError(f"Action {action.value} is not valid from state {state}.")
        return next_position

    def cost(self, state: Position, action: Action, next_state: Position) -> int:
        if self.result(state, action) != next_state:
            raise ValueError("Cost requested for an invalid transition.")
        return 1


@dataclass(frozen=True)
class SearchResult:
    path: list[Position]
    actions: list[Action]
    cost: int
    nodes_expanded: int


@dataclass(frozen=True)
class DeliveryPlan:
    actions: list[Action]
    cost: int
    nodes_expanded: int
    completed_delivery_ids: list[str]


SearchAlgorithm = Callable[[SearchProblem], SearchResult]


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def actions_from_path(path: list[Position]) -> list[Action]:
    actions: list[Action] = []
    for current, next_position in zip(path, path[1:]):
        dx = next_position.x - current.x
        dy = next_position.y - current.y
        for action, delta in ACTION_DELTAS.items():
            if delta == (dx, dy):
                actions.append(action)
                break
        else:
            raise ValueError(f"Positions {current} and {next_position} are not adjacent.")
    return actions
