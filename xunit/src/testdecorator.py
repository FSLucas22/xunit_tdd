from typing import Type, Callable, TypeVar
from xunit.src.testcase import TestCase


TestSubCase = TypeVar('TestSubCase', bound=TestCase)


def Test(test_cls: Type[TestCase],
         test_method: Callable[[TestSubCase], None],
         ) -> Callable[[TestSubCase], None]:
    test_name = test_method.__name__
    if not hasattr(test_cls, 'testNames') or test_cls.testNames == "":
        test_cls.testNames = test_name
        return test_method
    test_cls.testNames += " " + test_name
    return test_method
