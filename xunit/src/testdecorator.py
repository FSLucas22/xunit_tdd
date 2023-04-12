from typing import Type, TypeVar, ParamSpec, Callable
from xunit.src.testcase import TestCase

    
T = TypeVar('T', bound=TestCase)
P = ParamSpec('P')


class TestMethod:
    def __call__(self) -> None:
        pass


def getTestMethods(test_cls: Type[T]) -> str:
    for name, value in test_cls.__dict__.items():
        if type(value) == type:
            return name
    return "testMethod"


def Test(test_method: Callable[P, None]) -> Type[TestMethod]:
    return type('TestMethod', (TestMethod,), {
        '__call__': test_method
    })


def TestClass(test_cls: Type[T]) -> Type[T]:
    return test_cls
