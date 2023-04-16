from __future__ import annotations

from .consts import COLOUR_BINDINGS, KEY_BINDINGS, NUM_COLS, NUM_ROWS, START_POSITIONS
from .data_types import Colour, Coord, Direction

FORBIDDEN_ACTIONS = {
    Direction.RIGHT: Direction.LEFT,
    Direction.LEFT: Direction.RIGHT,
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
}


class Snake:
    def __init__(self, player_number: int) -> None:
        self.coords: list[Coord] = []
        self.crashed = False
        self.heading = Direction.RIGHT

        self.colour: Colour = COLOUR_BINDINGS[player_number]
        self.key_bindings: dict[str, Direction] = KEY_BINDINGS[0]
        self.player_number = player_number

    @property
    def head(self) -> Coord:
        return self.coords[-1]

    @property
    def tail(self) -> Coord:
        return self.coords[0]

    def reset_postition(self) -> None:
        self.coords = [START_POSITIONS[self.player_number]]
        self.crashed = False
        self.heading = Direction.RIGHT

    def set_from_msg(self, data: dict) -> None:
        update_coords = [Coord(coord[0], coord[1]) for coord in data["coords"]]
        self.coords[-4:] = update_coords[:-1]
        self.coords.append(update_coords[-1])
        self.crashed = data["crashed"]
        self.heading = Direction(data["heading"])

    def update_coords(self) -> None:
        if self.heading == Direction.UP:
            self.coords.append(Coord(self.head.x, self.head.y - 1))
        elif self.heading == Direction.DOWN:
            self.coords.append(Coord(self.head.x, self.head.y + 1))
        elif self.heading == Direction.LEFT:
            self.coords.append(Coord(self.head.x - 1, self.head.y))
        elif self.heading == Direction.RIGHT:
            self.coords.append(Coord(self.head.x + 1, self.head.y))
        # match self.heading:
        #     case Direction.UP:
        #         self.coords.append(Coord(self.head.x, self.head.y - 1))
        #     case Direction.DOWN:
        #         self.coords.append(Coord(self.head.x, self.head.y + 1))
        #     case Direction.LEFT:
        #         self.coords.append(Coord(self.head.x - 1, self.head.y))
        #     case Direction.RIGHT:
        #         self.coords.append(Coord(self.head.x + 1, self.head.y))

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
        if self.key_bindings.get(key) is None:
            return False
        return True

    def set_heading(self, key_pressed: str) -> None:
        self.heading = self.key_bindings[key_pressed]
