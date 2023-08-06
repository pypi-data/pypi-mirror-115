from typing import Iterable, Iterator

from overrides.overrides import overrides

from ..utils import Point2D
from .cell import Cell
from .grid import Grid


class DummyGrid(Grid):
    """
    Simple, empty grid. Can be used as a mock grid.
    """

    @overrides
    def _get_cell_or_raise(self, coord: Point2D) -> Cell:
        assert coord.x < self.dim.x
        assert coord.y < self.dim.y
        return Cell(pos=coord)

    @overrides
    def get_neighbours(self, cell: Point2D) -> Iterable[Cell]:
        return []  # we don't need the real values.

    @overrides
    def __iter__(self) -> Iterator[Cell]:
        values = (Cell(pos=Point2D(x=x, y=y))
                  for y in range(self.dim.y) for x in range(self.dim.x))
        # to-do check ordering
        return values
