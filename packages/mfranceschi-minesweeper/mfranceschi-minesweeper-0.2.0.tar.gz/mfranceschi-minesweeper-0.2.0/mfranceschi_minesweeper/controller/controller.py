from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ..model.utils import Point2D
from ..view.gui import GUI


@dataclass(frozen=True)
class DifficultyLevel:
    """
    A level of difficulty is defined by the grid size and the number of mines.
    """
    nbr_mines: int
    grid_dim: Point2D


class DifficultyLevels(Enum):
    """
    Enumeration of known difficulty levels.
    """
    EASY = DifficultyLevel(nbr_mines=10, grid_dim=Point2D(8, 8))
    INTERMEDIATE = DifficultyLevel(nbr_mines=40, grid_dim=Point2D(16, 16))
    EXPERT = DifficultyLevel(nbr_mines=99, grid_dim=Point2D(30, 16))


class Controller:
    """
    Abstract controller class.
    Provides infos about current game and processes user inputs.
    """

    def init_gui(self, gui: GUI) -> None:
        raise NotImplementedError()

    def on_new_game(self, difficulty_level: Optional[DifficultyLevel] = None) -> None:
        raise NotImplementedError()

    def on_left_click(self, cell_coord: Point2D) -> None:
        raise NotImplementedError()

    def on_right_click(self, cell_coord: Point2D) -> None:
        raise NotImplementedError()

    def get_nbr_mines(self) -> int:
        raise NotImplementedError()

    def get_current_game_time(self) -> float:
        raise NotImplementedError()
