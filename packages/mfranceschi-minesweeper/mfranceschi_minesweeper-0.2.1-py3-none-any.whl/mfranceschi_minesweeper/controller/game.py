from time import time
from typing import List, Optional

from ..model.cell import CellValue
from ..model.dummy_grid import DummyGrid
from ..model.fill_grid import GridFiller
from ..model.gridmanager import GridManager
from ..model.grid_impl_with_python_list import GridImplWithPythonList
from ..utils import Point2D
from .controller import DifficultyLevel


class Game:
    """
    An instance of a class contains a grid and metadata about a single game of minesweeper.
    It wraps helpers through methods and properties for hiding difficulty level and grid management.
    """

    MINIMAL_REVEALED_CELLS_WITH_ZERO_NEIGHBOURS = 5

    def __init__(self, difficulty: DifficultyLevel):
        self.difficulty = difficulty
        self.grid_manager = GridManager(grid_dim=difficulty.grid_dim)
        self.game_is_running = False
        self.game_starting_time = time()
        self.game_ending_time = time()

    @property
    def nbr_mines(self) -> int:
        return self.difficulty.nbr_mines

    @property
    def grid_dim(self) -> Point2D:
        return self.difficulty.grid_dim

    @property
    def count_of_cells_not_revealed(self) -> int:
        return self.grid_manager.get_count_of_not_revealed_cells()

    @property
    def grid_for_display(self) -> List[CellValue]:
        return self.grid_manager.get_grid_for_display()

    def get_game_time(self) -> float:
        if self.game_is_running:
            return time() - self.game_starting_time
        else:
            return self.game_ending_time - self.game_starting_time

    def check_cell_can_be_revealed(self, cell_coord: Point2D) -> bool:
        return self.grid_manager.check_cell_can_be_revealed(cell_coord)

    def check_cell_can_be_flagged_or_unflagged(self, cell_coord: Point2D) -> bool:
        return self.grid_manager.check_cell_can_be_flagged_or_unflagged(cell_coord)

    def check_cell_has_mine(self, cell_coord: Point2D) -> bool:
        return self.grid_manager.get_cell_has_mine(cell_coord)

    def reset_grid(
        self,
        origin_cell_position: Point2D,
        fill_grid_procedure: Optional[GridFiller] = None
    ) -> None:
        if fill_grid_procedure:
            GridManager.grid_impl = GridImplWithPythonList

            self.grid_manager = GridManager(self.grid_dim)
            self.grid_manager.fill_with_mines(fill_grid_procedure)

            # In normal minesweepers the grid is generated so that
            # the first user click is not on a mine + it reveals some cells around.
            while \
                    self.check_cell_has_mine(origin_cell_position) or \
                    self.grid_manager.get_count_of_close_zero_neighbours_cells(origin_cell_position) <= self.MINIMAL_REVEALED_CELLS_WITH_ZERO_NEIGHBOURS:  # pylint: disable=line-too-long
                self.grid_manager = GridManager(self.grid_dim)
                self.grid_manager.fill_with_mines(fill_grid_procedure)
        else:
            GridManager.grid_impl = DummyGrid
            self.grid_manager = GridManager(self.grid_dim)

    def reveal_all(self) -> None:
        self.grid_manager.reveal_all()

    def reveal_cell_if_possible(self, cell_coord: Point2D) -> bool:
        if self.grid_manager.check_cell_can_be_revealed(cell_coord):
            self.grid_manager.reveal_cell(cell_coord)
            return True
        else:
            return False

    def toggle_flag_if_possible(self, cell_coord: Point2D) -> bool:
        if self.check_cell_can_be_flagged_or_unflagged(cell_coord):
            self.grid_manager.toggle_flag_cell(cell_coord)
            return True
        else:
            return False

    def start_game(self) -> None:
        """
        Marks the game as started: the starting time is set.
        """

        self.game_is_running = True
        self.game_starting_time = time()

    def stop_game(self) -> None:
        """
        Marks the game as stopped: the whole grid is revealed and the ending time is set.
        """

        self.game_is_running = False
        self.game_ending_time = time()
        self.reveal_all()

    def is_won(self) -> bool:
        count_of_cells_not_revealed = self.grid_manager.get_count_of_not_revealed_cells()
        return self.nbr_mines == count_of_cells_not_revealed
