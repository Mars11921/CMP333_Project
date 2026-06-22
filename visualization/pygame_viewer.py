from __future__ import annotations

from simulator.campus_map import WALL
from simulator.environment import CampusEnvironment
from simulator.models import Position


class PygameViewer:
    def __init__(self, environment: CampusEnvironment, cell_size: int = 56) -> None:
        try:
            import pygame
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Pygame is not installed. Run: python3 -m pip install -r "
                "campus_robot_competition/requirements.txt"
            ) from exc

        self.pygame = pygame
        self.environment = environment
        self.cell_size = cell_size
        self.sidebar_width = 260
        self.width = environment.campus_map.width * cell_size + self.sidebar_width
        self.height = environment.campus_map.height * cell_size

        pygame.init()
        pygame.display.set_caption("Campus Robot Competition - Visual Demo")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 18)
        self.small_font = pygame.font.SysFont("arial", 15)

    def draw(self) -> None:
        self.screen.fill((248, 250, 252))
        self._draw_map()
        self._draw_deliveries()
        self._draw_robot()
        self._draw_sidebar()
        self.pygame.display.flip()

    def tick(self, frames_per_second: int = 30) -> None:
        self.clock.tick(frames_per_second)

    def handle_quit(self) -> bool:
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                return True
        return False

    def close(self) -> None:
        self.pygame.quit()

    def _draw_map(self) -> None:
        for y, row in enumerate(self.environment.campus_map.rows):
            for x, tile in enumerate(row):
                rect = self.pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                color = (31, 41, 55) if tile == WALL else (226, 232, 240)
                self.pygame.draw.rect(self.screen, color, rect)
                self.pygame.draw.rect(self.screen, (203, 213, 225), rect, 1)

    def _draw_deliveries(self) -> None:
        for index, delivery in enumerate(self.environment.deliveries, start=1):
            if (
                self.environment.robot.carrying_delivery_id != delivery.delivery_id
                and delivery.delivery_id not in self.environment.robot.completed_delivery_ids
            ):
                self._draw_marker(delivery.pickup, (22, 163, 74), f"P{index}")
            if delivery.delivery_id not in self.environment.robot.completed_delivery_ids:
                self._draw_marker(delivery.dropoff, (220, 38, 38), f"D{index}")

    def _draw_marker(self, position: Position, color: tuple[int, int, int], label: str) -> None:
        center = self._cell_center(position)
        self.pygame.draw.circle(self.screen, color, center, self.cell_size // 3)
        text = self.small_font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=center)
        self.screen.blit(text, text_rect)

    def _draw_robot(self) -> None:
        robot = self.environment.robot
        center = self._cell_center(robot.position)
        radius = self.cell_size // 3
        self.pygame.draw.circle(self.screen, robot.color, center, radius)
        self.pygame.draw.circle(self.screen, (15, 23, 42), center, radius, 2)
        if robot.carrying_delivery_id is not None:
            package_label = self._delivery_label(robot.carrying_delivery_id)
            package_rect = self.pygame.Rect(0, 0, self.cell_size // 3, self.cell_size // 4)
            package_rect.center = (center[0], center[1] - radius)
            self.pygame.draw.rect(self.screen, (245, 158, 11), package_rect, border_radius=3)
            self.pygame.draw.rect(self.screen, (120, 53, 15), package_rect, 1, border_radius=3)
            package_text = self.small_font.render(package_label, True, (15, 23, 42))
            package_text_rect = package_text.get_rect(center=package_rect.center)
            self.screen.blit(package_text, package_text_rect)
        label = self.font.render(robot.robot_id, True, (255, 255, 255))
        label_rect = label.get_rect(center=center)
        self.screen.blit(label, label_rect)

    def _draw_sidebar(self) -> None:
        left = self.environment.campus_map.width * self.cell_size
        panel = self.pygame.Rect(left, 0, self.sidebar_width, self.height)
        self.pygame.draw.rect(self.screen, (241, 245, 249), panel)
        self.pygame.draw.line(self.screen, (148, 163, 184), (left, 0), (left, self.height), 2)

        lines = [
            "Visual Demo",
            f"Step: {self.environment.step_count}",
            f"Robot: {self.environment.robot.robot_id}",
            f"Cost: {self.environment.robot.total_cost}",
            f"Carrying: {self.environment.robot.carrying_delivery_id or 'none'}",
            f"Completed: {len(self.environment.robot.completed_delivery_ids)}",
            "",
            "Recent events:",
        ]
        lines.extend(self.environment.events[-8:])

        y = 20
        for index, line in enumerate(lines):
            font = self.font if index == 0 else self.small_font
            color = (15, 23, 42) if index == 0 else (51, 65, 85)
            text = font.render(line, True, color)
            self.screen.blit(text, (left + 18, y))
            y += 28 if index == 0 else 22

    def _cell_center(self, position: Position) -> tuple[int, int]:
        return (
            position.x * self.cell_size + self.cell_size // 2,
            position.y * self.cell_size + self.cell_size // 2,
        )

    def _delivery_label(self, delivery_id: str) -> str:
        for index, delivery in enumerate(self.environment.deliveries, start=1):
            if delivery.delivery_id == delivery_id:
                return str(index)
        return "?"
