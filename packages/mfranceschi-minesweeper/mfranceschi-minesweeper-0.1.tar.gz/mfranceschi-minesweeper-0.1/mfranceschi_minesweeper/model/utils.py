from dataclasses import dataclass


@dataclass(frozen=True)
class Point2D:
    """
    2D coordinates in a grid.
    """

    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name
