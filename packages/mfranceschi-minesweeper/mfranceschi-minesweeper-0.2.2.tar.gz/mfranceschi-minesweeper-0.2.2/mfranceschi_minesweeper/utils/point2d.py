from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Point2D:
    """
    2D coordinates in a grid.
    """

    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name

    def __contains__(self, other: Any) -> bool:
        """
        Assuming other is also a Point2D, 
        returns whether both 'self' coordinates are > 'other' coordinates.
        """
        if isinstance(other, Point2D):
            other_point: Point2D = other
            return self.x > other_point.x and self.y > other_point.y
        else:
            return False
