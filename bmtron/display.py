from __future__ import annotations
import tkinter

from .consts import BOARD_HEIGHT, BOARD_WIDTH, NUM_COLS, NUM_ROWS
from .data_types import Colour
from .snake import Snake


class Display:
    def __init__(self, window: tkinter.Tk) -> None:
        self.canvas = tkinter.Canvas(window, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.canvas.pack()
        self.canvas.config(background=Colour.GREY)
        self.row_height = BOARD_HEIGHT / NUM_ROWS
        self.col_width = BOARD_WIDTH / NUM_COLS

    def clear(self) -> None:
        self.canvas.delete("all")

    def initialize_board(self) -> None:
        for i in range(NUM_ROWS):
            self.canvas.create_line(
                0, i * self.row_height, BOARD_WIDTH, i * self.row_height, fill=Colour.LIGHT_GREY
            )

        for i in range(NUM_COLS):
            self.canvas.create_line(
                i * self.col_width, 0, i * self.col_width, BOARD_HEIGHT, fill=Colour.LIGHT_GREY
            )

    def display_gameover(self, winner: Snake, time_taken: float) -> None:
        self.clear()
        score_text = "Scores \n"
        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.canvas.create_text(
            BOARD_WIDTH / 2,
            3 * BOARD_HEIGHT / 8,
            font="cmr 40 bold",
            fill=Colour.GREEN,
            text=score_text,
        )
        score_text = f"Winner: Player {winner.player_number + 1}\nScore: {len(winner.coords)}"
        self.canvas.create_text(
            BOARD_WIDTH / 2,
            1 * BOARD_HEIGHT / 2,
            font="cmr 50 bold",
            fill=Colour.BLUE,
            text=score_text,
        )
        time_spent = str(round(time_taken, 1)) + "sec"
        self.canvas.create_text(
            BOARD_WIDTH / 2,
            3 * BOARD_HEIGHT / 4,
            font="cmr 20 bold",
            fill=Colour.BLUE,
            text=time_spent,
        )
        score_text = "Click to play again \n"
        self.canvas.create_text(
            BOARD_WIDTH / 2,
            15 * BOARD_HEIGHT / 16,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )

    def display_snake(self, snake: Snake, draw_all: bool = False) -> None:
        if draw_all:
            for coord in snake.coords:
                x1 = coord.x * self.row_height
                y1 = coord.y * self.col_width
                x2 = x1 + self.row_height
                y2 = y1 + self.col_width
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=snake.colour, outline=snake.colour
                )
        else:
            # Only update last 5 sections
            for coord in snake.coords[-5:]:
                x1 = coord.x * self.row_height
                y1 = coord.y * self.col_width
                x2 = x1 + self.row_height
                y2 = y1 + self.col_width

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=snake.colour, outline=snake.colour
                )
