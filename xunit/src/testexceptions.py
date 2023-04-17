from typing import Type, Any


class InvalidAttributeException(Exception):
    pass


def expects(error_class: Type[Exception]) -> Any:
    ...
