from typing import Type, Callable, TypeVar
from xunit.src.testcase import TestCase


TestSubCase = TypeVar('TestSubCase', bound=TestCase)
TestMethod = Callable[[TestSubCase], None]

def Test(test_method: TestMethod[TestSubCase]) -> TestMethod[TestSubCase]:
    return test_method
