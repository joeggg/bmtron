from dataclasses import dataclass
from enum import Enum


@dataclass
class Coord:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash(f"{self.x},{self.y}")


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Colour(str, Enum):
    BLACK = "#FFFFFF"
    GREY = "#383838"
    RED = "#99453D"
    BLUE = "#376187"
    GREEN = "#7BC043"
    LIGHT_GREY = "#454545"
    LIGHT_RED = "#EE7E77"
    LIGHT_BLUE = "#67B0CF"
