from typing import List, Tuple

import pytest

from model.grid import Cell, Grid
from model.utils import Point2D


def test_it_has_correct_dimensions(grid_5_7: Grid):
    assert grid_5_7.dim.x == 5
    assert grid_5_7.dim.y == 7


class TestGetNeighbours:
    """
    Groups tests for Grid.get_neighbours(x, y)
    """

    @classmethod
    def check_list_of_cells(
            cls,
            list_to_review: List[Cell],
            cells_to_look_for: List[Tuple[int, int]],
            check_len: bool = True):
        if check_len:
            assert \
                len(list_to_review) == len(cells_to_look_for), \
                "Invalid amount of neighbours"

        for cell in cells_to_look_for:
            cell_pos = Point2D(x=cell[0], y=cell[1])
            assert \
                any(
                    cell_from_list for cell_from_list in list_to_review
                    if cell_from_list.x == cell_pos.x and cell_from_list.y == cell_pos.y
                ), \
                f"Unable to find cell of coordinates (x={cell_pos.x}, y={cell_pos.y}) " + \
                "within the list of neighbours"

    @staticmethod
    def test_raises_error_if_out_of_range(grid_5_7: Grid):
        # Negative values
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(Point2D(-1, 0))
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(Point2D(0, -1))
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(Point2D(-4, -4))

        # Equal to grid size
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(Point2D(grid_5_7.dim.x, 0))
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(Point2D(0, grid_5_7.dim.y))
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(Point2D(grid_5_7.dim.x, grid_5_7.dim.y))

        # More than grid size
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(Point2D(grid_5_7.dim.x + 1, 0))
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(Point2D(0, grid_5_7.dim.y + 1))
        with pytest.raises(AssertionError):
            grid_5_7.get_neighbours(
                Point2D(grid_5_7.dim.x + 4, grid_5_7.dim.y + 4))

    def test_for_corners(self, grid_5_7: Grid):
        # Top left
        self.check_list_of_cells(
            grid_5_7.get_neighbours(Point2D(0, 0)),
            [(0, 1), (1, 0), (1, 1)]
        )

        # Bottom left
        self.check_list_of_cells(
            grid_5_7.get_neighbours(Point2D(0, 6)),
            [(0, 5), (1, 6), (1, 5)]
        )

        # Top right
        self.check_list_of_cells(
            grid_5_7.get_neighbours(Point2D(4, 0)),
            [(3, 0), (4, 1), (3, 1)]
        )

        # Bottom right
        self.check_list_of_cells(
            grid_5_7.get_neighbours(Point2D(4, 6)),
            [(3, 6), (4, 5), (3, 6)]
        )

    def test_for_sides(self, grid_5_7: Grid):
        # Top
        self.check_list_of_cells(
            grid_5_7.get_neighbours(Point2D(2, 0)),
            [(1, 0), (1, 1), (2, 1), (3, 0), (3, 1)]
        )

        # Left
        self.check_list_of_cells(
            grid_5_7.get_neighbours(Point2D(0, 2)),
            [(0, 1), (0, 3), (1, 1), (1, 2), (1, 3)]
        )

        # Bottom
        self.check_list_of_cells(
            grid_5_7.get_neighbours(Point2D(2, 6)),
            [(1, 5), (1, 6), (2, 5), (3, 5), (3, 6)]
        )

        # Right
        self.check_list_of_cells(
            grid_5_7.get_neighbours(Point2D(4, 2)),
            [(3, 1), (3, 2), (3, 3), (4, 1), (4, 3)]
        )

    def test_all_other_cells(self, grid_5_7: Grid):
        for pos_x in range(1, grid_5_7.dim.x - 1):
            for pos_y in range(1, grid_5_7.dim.y - 1):
                self.check_list_of_cells(
                    grid_5_7.get_neighbours(Point2D(pos_x, pos_y)),
                    [
                        (pos_x-1, pos_y-1), (pos_x, pos_y-1), (pos_x+1, pos_y-1),
                        (pos_x-1, pos_y), (pos_x+1, pos_y),
                        (pos_x-1, pos_y+1), (pos_x, pos_y+1), (pos_x+1, pos_y+1),
                    ]
                )


def test_it_can_use_subscript_operator(grid_5_7: Grid):
    my_cell = grid_5_7[1, 2]
    assert my_cell.x == 1
    assert my_cell.y == 2
