import tkinter as tk
from typing import Callable, List

from ..model.cell import CellValue, CellValueAsString
from ..model.utils import Point2D
from .cell_view import CellView


class GridView(tk.Frame):
    """
    Renders a grid and intercepts user clicks on cells.
    """

    def __init__(
            self,
            size_x: int, size_y: int,
            on_left_click: Callable[[Point2D], None],
            on_right_click: Callable[[Point2D], None],
            **kwargs) -> None:
        super().__init__(**kwargs)
        self.size_x = size_x
        self.size_y = size_y
        self.on_left_click = on_left_click
        self.on_right_click = on_right_click

        for row_index in range(self.size_y):
            self.rowconfigure(row_index, minsize=25, weight=1)
        for column_index in range(self.size_x):
            self.columnconfigure(column_index, minsize=25, weight=1)

        self.buttons: List[CellView] = []

        for row_index in range(self.size_y):
            for column_index in range(self.size_x):
                coord = Point2D(x=column_index, y=row_index)

                button = CellView(
                    cell_coord=coord,
                    master=self,
                    on_left_click=self.on_left_click,
                    on_right_click=self.on_right_click)
                button.widget.grid(
                    row=row_index, column=column_index, sticky="nsew")
                self.buttons.append(button)

        self.cell_values: List[CellValue] = [
            CellValueAsString.NOT_REVEALED.value] * len(self.buttons)

    def _index_of_point(self, point: Point2D) -> int:
        return point.y * self.size_x + point.x

    def set_grid(self, grid: List[CellValue]) -> None:
        self.cell_values = grid
        for i, value in enumerate(grid):
            self.buttons[i].set_cell_value(value)

    def refresh(self) -> None:
        self.set_grid(self.cell_values)
