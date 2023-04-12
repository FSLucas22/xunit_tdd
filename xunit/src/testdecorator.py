from typing import Type, Callable, TypeVar, ParamSpec, NewType
from xunit.src.testcase import TestCase
from abc import ABC, abstractmethod

    
T = TypeVar('T', bound=TestCase)
P = ParamSpec('P')


class TestMethod:
    def __call__(self) -> None:
        pass


def Test(test_method: Callable[P, None]) -> Type[TestMethod]:
    return type('TestMethod', (TestMethod,), {
        '__call__': test_method
    })


def TestClass(test_cls: Type[T]) -> Type[T]:
    return test_cls
