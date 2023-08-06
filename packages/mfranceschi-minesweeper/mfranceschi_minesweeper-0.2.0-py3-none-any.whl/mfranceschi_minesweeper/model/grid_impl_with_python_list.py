from typing import Iterable, Iterator, List

from overrides.overrides import overrides

from .cell import Cell
from .grid import Grid
from .utils import Point2D


class GridImplWithPythonList(Grid):
    """
    Implementation of the Grid with a Python list.
    """

    def __init__(self, dim: Point2D):
        super().__init__(dim)

        self.grid: List[List[Cell]] = [
            [Cell(Point2D(x, y)) for x in range(dim.x)]
            for y in range(dim.y)
        ]

    @overrides
    def _get_cell_or_raise(self, coord: Point2D) -> Cell:
        assert 0 <= coord.x < self.dim.x
        assert 0 <= coord.y < self.dim.y
        return self.grid[coord.y][coord.x]

    @overrides
    def get_neighbours(self, cell: Point2D) -> Iterable[Cell]:
        neighbours = []
        max_x = self.dim.x - 1
        max_y = self.dim.y - 1

        x, y = cell.x, cell.y  # pylint: disable=invalid-name

        if x != 0:
            # Top left
            if y != 0:
                neighbours.append(self[x-1, y-1])

            # Left
            neighbours.append(self[x-1, y])

            # Bottom left
            if y != max_y:
                neighbours.append(self[x-1, y+1])

        # Top
        if y != 0:
            neighbours.append(self[x, y-1])

        # Bottom
        if y != max_y:
            neighbours.append(self[x, y+1])

        if x != max_x:
            # Top right
            if y != 0:
                neighbours.append(self[x+1, y-1])

            # Right
            neighbours.append(self[x+1, y])

            # Bottom right
            if y != max_y:
                neighbours.append(self[x+1, y+1])

        return neighbours

    @overrides
    def __iter__(self) -> Iterator[Cell]:
        return (cell for line in self.grid for cell in line)
