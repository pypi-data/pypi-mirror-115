from contextlib import contextmanager
from typing import Callable


@contextmanager
def do_after(action: Callable[[], None]):
    """Returns a context manager that simply calls the given action on exit."""
    yield None
    action()
