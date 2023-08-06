from time import time
from typing import Optional

from overrides import overrides

from ..model.fill_grid import RandomGridFiller
from ..model.gridmanager import GridManager
from ..model.utils import Point2D
from ..view.gui import GUI

from .controller import Controller, DifficultyLevel, DifficultyLevels


class ControllerImpl(Controller):
    """
    Actual implementation of a controller.
    Initial difficulty is easy.
    """

    INITIAL_DIFFICULTY = DifficultyLevels.EASY

    def __init__(self) -> None:
        self.gui: GUI
        self.grid_manager: GridManager
        self.difficulty: DifficultyLevel
        self.game_is_running: bool
        self.set_difficulty(self.INITIAL_DIFFICULTY.value)
        self.game_starting_time: float = time()
        self.game_ending_time: float = time()
        self._start_game()

    def set_difficulty(self, level: DifficultyLevel):
        self.difficulty = level

    @overrides
    def init_gui(self, gui: GUI) -> None:
        self.gui = gui
        self.on_new_game()

    @overrides
    def on_left_click(self, cell_coord: Point2D) -> None:
        if not self.grid_manager.check_cell_can_be_revealed(cell_coord):
            return

        self.grid_manager.reveal_cell(cell_coord)
        if self.grid_manager.get_cell_has_mine(cell_coord):
            self._stop_game()
            self.gui.set_grid(self.grid_manager.reveal_all())
            self.gui.game_over()
        else:
            self.gui.set_grid(self.grid_manager.get_grid_for_display())
            if self.has_won():
                self._stop_game()
                self.gui.set_grid(self.grid_manager.reveal_all())
                self.gui.victory()

    @overrides
    def on_right_click(self, cell_coord: Point2D) -> None:
        if not self.grid_manager.check_cell_can_be_flagged_or_unflagged(cell_coord):
            return

        self.grid_manager.toggle_flag_cell(cell_coord)
        self.gui.set_grid(self.grid_manager.get_grid_for_display())

    @overrides
    def on_new_game(self, difficulty_level: Optional[DifficultyLevel] = None) -> None:
        if difficulty_level:
            self.set_difficulty(difficulty_level)

        grid_dim = self.difficulty.grid_dim
        nbr_mines = self.difficulty.nbr_mines

        self.grid_manager = GridManager(grid_dim)
        self.grid_manager.fill_with_mines(
            nbr_mines=nbr_mines,
            procedure=RandomGridFiller(grid_dim)
        )
        self.gui.reset_grid_size(grid_dim)
        self.gui.set_nbr_mines(nbr_mines)
        self.gui.set_grid(self.grid_manager.get_grid_for_display())
        self._start_game()
        self.gui.game_starts()

    def has_won(self) -> bool:
        has_won = self.difficulty.nbr_mines == self.grid_manager.get_count_of_not_revealed_cells()
        return has_won

    @overrides
    def get_nbr_mines(self) -> int:
        return self.difficulty.nbr_mines

    @overrides
    def get_current_game_time(self) -> float:
        if self.game_is_running:
            return time() - self.game_starting_time
        else:
            return self.game_ending_time - self.game_starting_time

    def _start_game(self) -> None:
        self.game_is_running = True
        self.game_starting_time = time()

    def _stop_game(self) -> None:
        self.game_is_running = False
        self.game_ending_time = time()
