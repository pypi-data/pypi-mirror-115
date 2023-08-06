from abc import abstractmethod
import random
from typing import Callable, Set, Tuple

from overrides.overrides import overrides

from ..utils import Point2D


class GridFiller:
    """Base class for algorithms for filling a grid with mines."""

    def __init__(self, grid_dim: Point2D, nbr_mines: int) -> None:
        self.grid_dim = grid_dim
        self.nbr_mines = nbr_mines

    @abstractmethod
    def __call__(self, place_mine: Callable[[Point2D], None]) -> None:
        """To be implemented."""


class DummyGridFiller(GridFiller):
    """
    Fills the first line with mines. Fails if it results in too many mines!
    """

    @overrides
    def __call__(self, place_mine: Callable[[Point2D], None]) -> None:
        x_cell = 0
        y_cell = 0

        for __ in range(self.nbr_mines):
            try:
                place_mine(Point2D(x_cell, y_cell))
                x_cell += 1
            except AssertionError:
                x_cell = 0
                y_cell += 1
                place_mine(Point2D(x_cell, y_cell))
                x_cell += 1


class RandomGridFiller(GridFiller):
    """
    Randomly fills the grid with no duplicates.
    """

    def __init__(self, grid_dim: Point2D, nbr_mines: int) -> None:
        super().__init__(grid_dim=grid_dim, nbr_mines=nbr_mines)
        self.placed_mines: Set[Tuple[int, int]] = set()

    @overrides
    def __call__(self, place_mine: Callable[[Point2D], None]) -> None:
        self.placed_mines = set()

        for __ in range(self.nbr_mines):
            position = Point2D(*self._make_position())
            place_mine(position)

    def _make_position(self) -> Tuple[int, int]:
        position = self._make_new_random_position()
        while position in self.placed_mines:
            position = self._make_new_random_position()
        self.placed_mines.add(position)
        return position

    def _make_new_random_position(self) -> Tuple[int, int]:
        return (random.randint(0, self.grid_dim.x - 1),
                random.randint(0, self.grid_dim.y - 1))
