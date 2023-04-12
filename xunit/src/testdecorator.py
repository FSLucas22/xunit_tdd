from typing import Type, Callable, TypeVar, Generic
from xunit.src.testcase import TestCase


T = TypeVar('T', bound=TestCase)


class TestMethod:
    pass


def Test(test_method: Callable[[T], None]) -> Callable[[T], None]:
    return test_method


def TestClass(test_cls: Type[T]) -> Type[T]:
    return test_cls
