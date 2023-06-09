from __future__ import annotations

from .consts import (
    COLOUR_BINDINGS,
    KEY_BINDINGS,
    NUM_COLS,
    NUM_ROWS,
    SNAKE_INITIAL_LENGTH,
)
from .types import Colour, Coord, Direction


class Snake:
    def __init__(self, player_number: int) -> None:
        self.coords: list[Coord] = []
        self.crashed = False
        self.heading = Direction.RIGHT
        self.object_ids: list[int] = []
        self.forbidden_actions = {
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT,
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
        }

        self.colour: Colour = COLOUR_BINDINGS[player_number]
        self.key_bindings: dict[str, Direction] = KEY_BINDINGS[player_number]
        self.player_number = player_number

    @property
    def head(self) -> Coord:
        return self.coords[-1]

    @property
    def tail(self) -> Coord:
        return self.coords[0]

    def reset_postition(self) -> None:
        self.coords = [Coord(i, 5 * self.player_number) for i in range(SNAKE_INITIAL_LENGTH)]
        self.object_ids = []
        self.crashed = False
        self.heading = Direction.RIGHT

    def update_coords(self) -> None:
        match self.heading:
            case Direction.UP:
                self.coords.append(Coord(self.head.x, self.head.y - 1))
            case Direction.DOWN:
                self.coords.append(Coord(self.head.x, self.head.y + 1))
            case Direction.LEFT:
                self.coords.append(Coord(self.head.x - 1, self.head.y))
            case Direction.RIGHT:
                self.coords.append(Coord(self.head.x + 1, self.head.y))

    def check_if_crashed(self, snakes: list[Snake]) -> None:
        # Check if it hit the wall or a snake's body
        if any(
            [
                self.head.x > NUM_COLS - 1,
                self.head.x < 0,
                self.head.y > NUM_ROWS - 1,
                self.head.y < 0,
                len(set(self.coords)) != len(self.coords),
            ]
        ):
            self.crashed = True
            return

        for snake in snakes:
            if snake.player_number == self.player_number:
                continue
            for coord in snake.coords:
                if self.head == coord:
                    self.crashed = True
                    return

    def is_key_valid(self, key: str) -> bool:
        if (direction := self.key_bindings.get(key)) is None:
            return False

        if self.forbidden_actions[self.heading] == direction:
            return False

        return True

    def set_heading(self, key_pressed: str) -> None:
        self.heading = self.key_bindings[key_pressed]
