from typing import Type, Iterator
from contextlib import contextmanager


class InvalidAttributeException(Exception):
    pass


class ExpectationError(Exception):
    pass


class InvalidPathError(Exception):
    pass


@contextmanager
def expects(error_class: Type[Exception]) -> Iterator[None]:
    try:
        yield
    except error_class as e:
        return
    raise ExpectationError(
        f"Did not raised {error_class.__name__}"
    )
