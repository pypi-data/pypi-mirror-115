from dataclasses import dataclass
import functools
import sys
import typing
from typing import Any, Optional


@dataclass(frozen=True)
class Point2D:
    """
    2D coordinates in a grid.
    """

    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name


class ConditionalDecorator:
    """
    Helper for decorator available on condition.
    Condition is evaluated only once, at construction time.
    """

    def __init__(
            self,
            decorator_if_true: Optional[Any],
            decorator_if_false: Optional[Any],
            condition: bool
    ) -> None:
        self.actual_decorator = decorator_if_true if condition else decorator_if_false
        self.condition = condition

    def __call__(self, func) -> Any:
        return self.actual_decorator(func) if self.actual_decorator else func


class CacheDecorator(ConditionalDecorator):
    """
    Decorator for setting a cache on a function. 
    Uses functools' 'lru_cache' or 'cache'.
    """

    def __init__(self):
        super().__init__(decorator_if_true=functools.lru_cache(maxsize=None),
                         decorator_if_false=getattr(functools, "cache", None),
                         condition=sys.version_info.minor < 9)


class FinalDecorator(ConditionalDecorator):
    """
    Annotates a method as final, if available.
    """

    def __init__(self) -> None:
        super().__init__(decorator_if_true=getattr(typing, "final", None),
                         decorator_if_false=None,
                         condition=sys.version_info.minor >= 9)
