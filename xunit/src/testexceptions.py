from typing import Type, Any
from contextlib import contextmanager


class InvalidAttributeException(Exception):
    pass


@contextmanager
def expects(error_class: Type[Exception]) -> Any:
    try:
        yield
    except error_class as e:
        pass
