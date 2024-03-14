import contextlib
from typing import Callable


def suppress_connection_errors(func: Callable):
    def wrapper(*args, **kwargs):
        with contextlib.suppress(ConnectionResetError, ConnectionAbortedError):
            func(*args, **kwargs)
    return wrapper
