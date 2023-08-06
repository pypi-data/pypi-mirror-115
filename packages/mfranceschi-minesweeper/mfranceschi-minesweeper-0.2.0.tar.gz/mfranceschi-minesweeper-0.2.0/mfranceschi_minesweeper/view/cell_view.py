import tkinter as tk
from typing import Callable

from ..model.cell import CellValue, CellValueAsString
from ..model.utils import Point2D
from .cell_button_configurator import CellButtonConfigurator, MfranCellButtonConfigurator


class CellView:
    """
    Wrapper class: configures a cell button.
    When the cell updates please set the "cell_value" string.
    """

    cell_button_configurator: CellButtonConfigurator = MfranCellButtonConfigurator()

    def __init__(
            self,
            cell_coord: Point2D,
            master: tk.Widget,
            on_left_click: Callable[[Point2D], None],
            on_right_click: Callable[[Point2D], None]
    ):
        self.widget = tk.Button(master=master)
        self.cell_coord = cell_coord
        self.on_left_click = on_left_click
        self.on_right_click = on_right_click
        self.set_cell_value(CellValueAsString.NOT_REVEALED.value)

        self.widget.bind("<ButtonRelease>", self.handle_button_event)

    def handle_button_event(self, event: tk.Event):
        if event.num == 1:
            # Left click
            self.on_left_click(self.cell_coord)
        elif event.num == 2 or event.num == 3:
            # Middle or right click
            self.on_right_click(self.cell_coord)

    def set_cell_value(self, cell_value: CellValue) -> None:
        self.cell_button_configurator.configure_button(self.widget, cell_value)
