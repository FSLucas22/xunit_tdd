from typing import Type, Callable, TypeVar, Generic
from xunit.src.testcase import TestCase


T = TypeVar('T', bound=TestCase)


def Test(test_method: Callable[[T], None]) -> Callable[[T], None]:
    return test_method
