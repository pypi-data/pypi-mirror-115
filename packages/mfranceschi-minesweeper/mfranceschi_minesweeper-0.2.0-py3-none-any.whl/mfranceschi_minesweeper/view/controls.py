import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

from ..controller.controller import Controller, DifficultyLevel, DifficultyLevels
from ..view.cell_button_configurator import MfranCellButtonConfigurator, \
    WindowsXpCellButtonConfigurator
from .cell_view import CellView


class NewGameButton(tk.Button):
    """
    Wraps a button. On click, calls the given command to start a new game.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(background="yellow", *args, **kwargs)


class NbrMinesLabel(tk.Label):
    """
    Wraps a label with the number of mines.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _make_string_for_nbr_mines(nbr: int) -> str:
        return f"There are {nbr} mines!"

    def set_nbr_mines(self, nbr: int) -> None:
        self.configure(text=self._make_string_for_nbr_mines(nbr))


class DifficultyChoice(tk.Frame):
    """
    Wraps a frame that allows the user to select a difficulty
    and start a new game with it.
    """

    def __init__(
        self,
        on_new_difficulty: Callable[[DifficultyLevel], None],
        *args: Any, **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.on_new_difficulty = on_new_difficulty

        self.listbox = tk.Listbox(
            master=self, selectmode=tk.SINGLE, width=0, height=0)
        choices = [x.name.title() for x in DifficultyLevels]
        self.listbox.insert(tk.END, *choices)
        self.listbox.selection_anchor(0)
        self.listbox.pack()

        self.ok_button = tk.Button(
            master=self, text="OK (new game)", command=self._handle_ok)
        self.ok_button.pack()

    def _handle_ok(self):
        choice: str = str(self.listbox.get(tk.ANCHOR)).upper()
        assert choice in DifficultyLevels.__members__.keys()
        self.on_new_difficulty(getattr(DifficultyLevels, choice).value)


class ElapsedTimeLabel(tk.Label):
    """
    Wraps a label with the elapsed time, straight from the text variable.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ColourPaletteChoice(tk.Frame):
    """Widget with a label and a combo box for changing the colours of the grid."""

    def __init__(self, on_change: Callable[[str], None] = None, **kwargs):
        super().__init__(**kwargs)
        choices = ["Mfranceschi (default)", "Windows XP"]

        self.value = tk.StringVar(master=self, value=choices[0])

        label = tk.Label(master=self, text="Change theme")
        label.grid(column=0, row=0)

        self.combo_box = ttk.Combobox(
            master=self,
            values=choices, textvariable=self.value,)
        self.combo_box.bind('<<ComboboxSelected>>',
                            self._handle_change)
        self.combo_box.grid(row=1, column=0)
        self.on_change = on_change

    def _handle_change(self, _event):
        self.on_change(self.value.get())


class ControlsWidget(tk.Frame):
    """
    Wraps some cool widgets that display stuff or provide the user with input items.
    """

    def __init__(
            self,
            controller: Controller,
            elapsed_time_text: tk.StringVar,
            refresh_grid: Callable[[], None],
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.configure(padx=15, pady=15, background="light cyan")

        self.new_game_button = NewGameButton(
            master=self, command=controller.on_new_game, text="New game")
        self.new_game_button.grid(row=0, column=0, rowspan=2)

        self.nbr_mines_label = NbrMinesLabel(master=self)
        self.nbr_mines_label.set_nbr_mines(controller.get_nbr_mines())
        self.nbr_mines_label.grid(row=2, column=0, pady=5)

        self.elapsed_time_label = ElapsedTimeLabel(
            master=self, textvariable=elapsed_time_text)
        self.elapsed_time_label.grid(row=3, column=0, pady=5)

        self.difficulty_choice = DifficultyChoice(
            master=self, on_new_difficulty=controller.on_new_game)
        self.difficulty_choice.grid(row=4, column=0, pady=20)

        def on_change_colour_palette(new_value: str):
            if "XP" in new_value:
                CellView.cell_button_configurator = WindowsXpCellButtonConfigurator()
            else:
                CellView.cell_button_configurator = MfranCellButtonConfigurator()
            refresh_grid()

        self.colour_palette_choice = ColourPaletteChoice(
            master=self, on_change=on_change_colour_palette)
        self.colour_palette_choice.grid(row=5, column=0, pady=5)

    def set_nbr_mines(self, nbr: int) -> None:
        self.nbr_mines_label.set_nbr_mines(nbr)
