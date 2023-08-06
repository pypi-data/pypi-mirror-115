from typing import ClassVar, List, Set, Type

from ..utils import Point2D
from .cell import Cell, CellValue, CellValueAsString
from .dummy_grid import DummyGrid
from .fill_grid import GridFiller
from .grid import Grid


class GridManager:
    """
    Manages a grid and provides convenience access methods.
    """

    grid_impl: ClassVar[Type[Grid]] = DummyGrid

    def __init__(self, grid_dim: Point2D):
        self._grid: Grid = self.grid_impl(grid_dim)
        self.nbr_mines = 0

    # GETTERS
    def get_grid_for_display(self) -> List[CellValue]:
        return [self._cell_to_string(cell) for cell in self._grid]

    def get_cell_has_mine(self, cell_coord: Point2D) -> bool:
        return self._grid.get_cell_has_mine(cell_coord)

    def get_count_of_not_revealed_cells(self) -> int:
        return len([cell for cell in self._grid if not cell.is_revealed])

    def _cell_to_string(self, cell: Cell) -> CellValue:
        if cell.is_revealed:
            if cell.has_mine:
                return CellValueAsString.MINE.value
            else:
                close_mines = self._grid.get_nb_of_close_mines(cell.pos)
                return close_mines if close_mines else "0"
        elif cell.is_flagged:
            return CellValueAsString.FLAGGED.value
        else:
            return CellValueAsString.NOT_REVEALED.value

    # UNITARY SETTERS
    def toggle_flag_cell(self, cell_coord: Point2D) -> None:
        cell = self._grid[cell_coord.x, cell_coord.y]
        if not cell.is_revealed:
            self._grid.set_cell_flagged(cell_coord, not cell.is_flagged)

    def _set_cell_has_mine(self, cell_coord: Point2D) -> None:
        self._grid[cell_coord.x, cell_coord.y].has_mine = True

    # GLOBAL MODIFIERS
    def fill_with_mines(self, grid_filler: GridFiller) -> None:
        grid_filler(self._set_cell_has_mine)

        assert len([cell for cell in self._grid if cell.has_mine]) == grid_filler.nbr_mines, \
            "Unexpected number of cells with a mine after filling the grid!"

    def reveal_all(self) -> None:
        for cell in self._grid:
            cell.is_revealed = True

    def get_count_of_close_zero_neighbours_cells(self, starting_cell_pos: Point2D) -> int:
        """
        Returns the number of cells, including the 'starting_cell', 
        which are neighbours to the 'starting_cell' and that have no close mines.
        """
        visited_cells: Set[Point2D] = set()

        def visit_cell(cell_pos: Point2D):
            """
            If this cell has not been visited and has zero mines in the immediate neighbourhood,
            mark it as visited and visit its neighbours.
            """

            if cell_pos in visited_cells or self._grid.get_nb_of_close_mines(cell_pos):
                return

            visited_cells.add(cell_pos)

            if cell_pos.x != 0:
                pos_to_check = Point2D(cell_pos.x-1, cell_pos.y)
                visit_cell(pos_to_check)
            if cell_pos.y != 0:
                pos_to_check = Point2D(cell_pos.x, cell_pos.y-1)
                visit_cell(pos_to_check)
            if cell_pos.x != self._grid.dim.x - 1:
                pos_to_check = Point2D(cell_pos.x+1, cell_pos.y)
                visit_cell(pos_to_check)
            if cell_pos.y != self._grid.dim.y - 1:
                pos_to_check = Point2D(cell_pos.x, cell_pos.y+1)
                visit_cell(pos_to_check)

        visit_cell(starting_cell_pos)
        return len(visited_cells)

    class CellRevealer:  # pylint: disable=too-few-public-methods
        """
        This class wraps the cell revealing logic if it has to be done recursively.
        Invoke the run() method on click on some cell with no neighbour.
        """

        def __init__(self, grid: Grid) -> None:
            self.grid = grid
            self.explored_no_neighbours: Set[Point2D] = set()

        def run(self, cell_coord: Point2D) -> None:
            self.explored_no_neighbours.add(cell_coord)
            self.grid.set_cell_revealed(cell_coord, True)

            local_neighbours = self.grid.get_neighbours(cell_coord)
            for neighbour_cell in local_neighbours:
                neighbour_cell_pos = neighbour_cell.pos

                if neighbour_cell_pos in self.explored_no_neighbours:
                    continue

                if self.grid.get_nb_of_close_mines(neighbour_cell_pos) == 0:
                    self.run(
                        cell_coord=neighbour_cell_pos)
                else:
                    self.grid.set_cell_revealed(neighbour_cell_pos, True)

    def reveal_cell(self, cell_coord: Point2D) -> None:
        cell = self._grid[cell_coord.x, cell_coord.y]
        if not cell.is_revealed and not cell.is_flagged:
            self._grid.set_cell_revealed(cell_coord, True)
        if not cell.has_mine and self._grid.get_nb_of_close_mines(cell_coord) == 0:
            self.CellRevealer(grid=self._grid).run(cell_coord=cell_coord)

    def check_cell_can_be_revealed(self, cell_coord: Point2D) -> bool:
        cell = self._grid[cell_coord.x, cell_coord.y]
        return not cell.is_revealed and not cell.is_flagged

    def check_cell_can_be_flagged_or_unflagged(self, cell_coord: Point2D) -> bool:
        cell = self._grid[cell_coord.x, cell_coord.y]
        return not cell.is_revealed
