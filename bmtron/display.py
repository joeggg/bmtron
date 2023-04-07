import tkinter

from .consts import BOARD_SIZE, NUM_COLS, NUM_ROWS
from .snake import Snake
from .data_types import Colour, Coord


class Display:
    def __init__(self, window: tkinter.Tk) -> None:
        self.canvas = tkinter.Canvas(window, width=BOARD_SIZE, height=BOARD_SIZE)
        self.canvas.pack()
        self.board: list[Coord] = []

    def clear(self) -> None:
        self.canvas.delete("all")

    def initialize_board(self):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                self.board.append((i, j))

        for i in range(NUM_ROWS):
            self.canvas.create_line(
                i * BOARD_SIZE / NUM_ROWS, 0, i * BOARD_SIZE / NUM_ROWS, BOARD_SIZE
            )

        for i in range(NUM_COLS):
            self.canvas.create_line(
                0, i * BOARD_SIZE / NUM_COLS, BOARD_SIZE, i * BOARD_SIZE / NUM_COLS
            )

    def display_gameover(self, winner: Snake, time_taken: float) -> None:
        self.canvas.delete("all")
        score_text = "Scores \n"
        # put gif image on canvas
        # pic's upper left corner (NW) on the canvas is at x=50 y=10
        self.canvas.create_text(
            BOARD_SIZE / 2,
            3 * BOARD_SIZE / 8,
            font="cmr 40 bold",
            fill=Colour.GREEN,
            text=score_text,
        )
        score_text = f"Winner: Player {winner.player_number}\nScore: {len(winner.coords)}"
        self.canvas.create_text(
            BOARD_SIZE / 2,
            1 * BOARD_SIZE / 2,
            font="cmr 50 bold",
            fill=Colour.BLUE,
            text=score_text,
        )
        time_spent = str(round(time_taken, 1)) + "sec"
        self.canvas.create_text(
            BOARD_SIZE / 2,
            3 * BOARD_SIZE / 4,
            font="cmr 20 bold",
            fill=Colour.BLUE,
            text=time_spent,
        )
        score_text = "Click to play again \n"
        self.canvas.create_text(
            BOARD_SIZE / 2,
            15 * BOARD_SIZE / 16,
            font="cmr 20 bold",
            fill="gray",
            text=score_text,
        )

    def display_snake(self, snake: Snake, draw_all: bool = False) -> None:
        if draw_all:
            for coord in snake.coords:
                row_h = int(BOARD_SIZE / NUM_ROWS)
                col_w = int(BOARD_SIZE / NUM_COLS)
                x1 = coord.x * row_h
                y1 = coord.y * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                snake.object_ids.append(
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill=snake.colour, outline=Colour.BLACK
                    )
                )
        else:
            # Only update head
            coord = snake.coords[-1]
            row_h = int(BOARD_SIZE / NUM_ROWS)
            col_w = int(BOARD_SIZE / NUM_COLS)
            x1 = coord.x * row_h
            y1 = coord.y * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            snake.object_ids.append(
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=snake.colour, outline=Colour.RED)
            )
