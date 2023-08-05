import pytest

from model.grid import Grid
from model.grid_impl_with_python_list import GridImplWithPythonList
from model.utils import Point2D


@pytest.fixture
def grid_5_7() -> Grid:
    return GridImplWithPythonList(Point2D(5, 7))
