from __future__ import annotations
from .data_types import Colour, Direction


BOARD_WIDTH = 1000
BOARD_HEIGHT = 700
NUM_ROWS = 35
NUM_COLS = 50

UPDATE_DELAY_MS = 90

SNAKE_INITIAL_LENGTH = 3

COLOUR_BINDINGS: dict[int, Colour] = {
    0: Colour.RED,
    1: Colour.BLUE,
    2: Colour.GREEN,
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
