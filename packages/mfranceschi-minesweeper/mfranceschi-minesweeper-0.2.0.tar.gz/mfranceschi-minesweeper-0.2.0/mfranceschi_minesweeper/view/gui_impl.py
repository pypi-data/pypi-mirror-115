import tkinter as tk
from typing import List

from overrides import overrides

from ..controller.controller import Controller
from ..model.utils import Point2D
from .controls import ControlsWidget
from .grid_view import GridView
from .gui import CellValue, GUI

WIN_WIDTH = 500


class GUIImpl(GUI):
    """
    Actual implementation of the GUI.
    """

    def __init__(
            self,
            grid_dim: Point2D,
            controller: Controller
    ) -> None:
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Mfranceschi Minesweeper!")

        self.elapsed_time_text = tk.StringVar(master=self.root, value="")
        self._update_elapsed_time_text()

        self.make_grid_view(dim=grid_dim)
        self.make_controls_widget()

    @overrides
    def set_grid(self, grid: List[CellValue]) -> None:
        self.grid_view.set_grid(grid)

    def _update_elapsed_time_text(self):
        elapsed_seconds = self.controller.get_current_game_time()
        minutes, seconds = divmod(int(elapsed_seconds), 60)
        self.elapsed_time_text.set(
            f"Elapsed time: {f'{minutes}min ' if minutes else ''}{seconds}s")
        self.root.after(800, self._update_elapsed_time_text)

    @overrides
    def reset_grid_size(self, grid_dim: Point2D) -> None:
        self.grid_view.destroy()
        self.make_grid_view(dim=grid_dim)

    @overrides
    def set_nbr_mines(self, nbr_mines: int) -> None:
        self.controls_widget.set_nbr_mines(nbr_mines)

    @overrides
    def victory(self) -> None:
        self.root.configure(bg="green")

    @overrides
    def game_over(self) -> None:
        self.root.configure(bg="brown")

    @overrides
    def game_starts(self) -> None:
        self.root.configure(bg="sky blue")

    def make_grid_view(self, dim: Point2D) -> None:
        self.grid_view = GridView(
            master=self.root,
            height=WIN_WIDTH,
            bg="red",

            size_x=dim.x,
            size_y=dim.y,
            on_left_click=self.controller.on_left_click,
            on_right_click=self.controller.on_right_click,
        )
        self.grid_view.grid(column=1, row=0)

    def make_controls_widget(self) -> None:
        self.controls_widget = ControlsWidget(
            master=self.root,
            height=30,
            bg="blue",

            controller=self.controller,
            elapsed_time_text=self.elapsed_time_text,
            refresh_grid=lambda: self.grid_view.refresh()  # pylint: disable=unnecessary-lambda
        )
        self.controls_widget.grid(column=0, row=0)
