from typing import Type, TypeVar, ParamSpec, Callable
from xunit.src.testcase import TestCase

    
T = TypeVar('T', bound=TestCase)
P = ParamSpec('P')


class TestMethod:
    def __call__(self) -> None:
        pass


def getTestMethods(test_cls: Type[T]) -> str:
    names = []
    for name, value in test_cls.__dict__.items():
        if type(value) == type and issubclass(value, TestMethod):
            names.append(name)
    return ' '.join(names)


def Test(test_method: Callable[P, None]) -> Type[TestMethod]:
    return type('TestMethod', (TestMethod,), {
        '__call__': test_method
    })


def TestClass(test_cls: Type[T]) -> Type[T]:
    test_cls.testNames = getTestMethods(test_cls)
    return test_cls
