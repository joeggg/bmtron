from __future__ import annotations
from .data_types import Colour, Coord, Direction


BOARD_WIDTH = 1000
BOARD_HEIGHT = 700
NUM_ROWS = 35
NUM_COLS = 50

UPDATE_DELAY_MS = 90

START_POSITIONS = [
    Coord(15, 10),
    Coord(35, 10),
    Coord(15, 25),
    Coord(35, 25),
]

COLOUR_BINDINGS: dict[int, Colour] = {
    0: Colour.RED,
    1: Colour.BLUE,
    2: Colour.GREEN,
    3: Colour.LIGHT_BLUE,
}

KEY_BINDINGS: dict[int, dict[str, Direction]] = {
    0: {
        "w": Direction.UP,
        "s": Direction.DOWN,
        "a": Direction.LEFT,
        "d": Direction.RIGHT,
    },
    1: {
        "Up": Direction.UP,
        "Down": Direction.DOWN,
        "Left": Direction.LEFT,
        "Right": Direction.RIGHT,
    },
    2: {
        "i": Direction.UP,
        "k": Direction.DOWN,
        "j": Direction.LEFT,
        "l": Direction.RIGHT,
    },
}
