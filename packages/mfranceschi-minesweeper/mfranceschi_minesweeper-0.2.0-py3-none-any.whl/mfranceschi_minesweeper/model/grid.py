from abc import ABC, abstractmethod
from typing import Iterable, Iterator, Tuple

from overrides.enforce import EnforceOverrides

from .cell import Cell
from .utils import CacheDecorator, Point2D


class Grid(ABC, EnforceOverrides):
    """
    Container for a 2D grid of cells.
    Use __getitem__(x, y) to get a specific cell.
    """

    def __init__(self, dim: Point2D):
        assert dim.x >= 2
        assert dim.y >= 2
        self.dim = dim

    @abstractmethod
    def _get_cell_or_raise(self, coord: Point2D) -> Cell:
        raise NotImplementedError()

    def __getitem__(self, coord_xy: Tuple[int, int]) -> Cell:
        return self._get_cell_or_raise(Point2D(*coord_xy))

    @abstractmethod
    def get_neighbours(self, cell: Point2D) -> Iterable[Cell]:
        raise NotImplementedError()

    @CacheDecorator()
    def get_nb_of_close_mines(self, cell_coord: Point2D) -> int:
        assert not self.get_cell_has_mine(cell_coord)
        return sum((cell.has_mine for cell in self.get_neighbours(cell_coord)))

    def set_cell_flagged(self, cell_coord: Point2D, flagged: bool) -> None:
        self._get_cell_or_raise(cell_coord).is_flagged = flagged

    def set_cell_revealed(self, cell_coord: Point2D, revealed: bool) -> None:
        self._get_cell_or_raise(cell_coord).is_revealed = revealed

    def get_cell_has_mine(self, cell_coord: Point2D) -> bool:
        return self._get_cell_or_raise(cell_coord).has_mine

    @abstractmethod
    def __iter__(self) -> Iterator[Cell]:
        raise NotImplementedError()
