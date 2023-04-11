from typing import Type, Callable, TypeVar
from xunit.src.testcase import TestCase


TestSubCase = TypeVar('TestSubCase', bound=TestCase)


def Test(test_method: Callable[[TestSubCase], None],
         test_cls: Type[TestCase]) -> None:
    pass
