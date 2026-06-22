from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from simulator.models import Position


WALL = "#"
CORRIDOR = "."
VALID_TILES = {WALL, CORRIDOR}


@dataclass(frozen=True)
class CampusMap:
    rows: tuple[str, ...]

    @property
    def width(self) -> int:
        return len(self.rows[0])

    @property
    def height(self) -> int:
        return len(self.rows)

    def in_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def tile_at(self, position: Position) -> str:
        if not self.in_bounds(position):
            return WALL
        return self.rows[position.y][position.x]

    def is_walkable(self, position: Position) -> bool:
        return self.in_bounds(position) and self.tile_at(position) != WALL


def load_campus_map(path: str | Path) -> CampusMap:
    rows = tuple(
        line.rstrip("\n")
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    if not rows:
        raise ValueError("Campus map is empty.")

    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("All campus map rows must have the same width.")

    for y, row in enumerate(rows):
        for x, tile in enumerate(row):
            if tile not in VALID_TILES:
                raise ValueError(
                    f"Invalid map tile {tile!r} at ({x}, {y}). "
                    "Maps may only use '#' for walls and '.' for corridors."
                )

    return CampusMap(rows=rows)
