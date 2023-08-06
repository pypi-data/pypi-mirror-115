import random
from typing import Callable, Set, Tuple

from overrides.overrides import overrides

from .utils import Point2D


def fill_grid_dummy(function: Callable[[Point2D], None], nbr_mines: int) -> None:
    """
    Fills the first line with mines. Fails if it results in too many mines!
    """
    x_cell = 0
    y_cell = 0

    for __ in range(nbr_mines):
        try:
            function(Point2D(x_cell, y_cell))
            x_cell += 1
        except AssertionError:
            x_cell = 0
            y_cell += 1
            function(Point2D(x_cell, y_cell))
            x_cell += 1


class RandomGridFiller:
    """
    Call my constructor with the grid size.
    My call method randomly fills the grid with no duplicates.
    """

    def __init__(self, grid_dim: Point2D) -> None:
        self.grid_dim = grid_dim
        self.placed_mines: Set[Tuple[int, int]] = set()

    def make_new_random_position(self) -> Tuple[int, int]:
        return (random.randint(0, self.grid_dim.x - 1),
                random.randint(0, self.grid_dim.y - 1))

    def make_position(self) -> Tuple[int, int]:
        position = self.make_new_random_position()
        while position in self.placed_mines:
            position = self.make_new_random_position()
        self.placed_mines.add(position)
        return position

    @overrides
    def __call__(self, place_mine: Callable[[Point2D], None], nbr_mines: int) -> None:
        self.placed_mines = set()

        for __ in range(nbr_mines):
            place_mine(Point2D(*self.make_position()))
