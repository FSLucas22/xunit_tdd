from typing import Type, Any, Iterator
from contextlib import contextmanager


class InvalidAttributeException(Exception):
    pass


@contextmanager
def expects(error_class: Type[Exception]) -> Iterator[None]:
    try:
        yield
    except error_class as e:
        return
    raise Exception
