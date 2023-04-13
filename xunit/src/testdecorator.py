from typing import Type, TypeVar, ParamSpec, Callable
from xunit.src.testcase import TestCase
from xunit.src.testexceptions import InvalidAttributeException

    
T = TypeVar('T', bound=TestCase)
P = ParamSpec('P')


def getTestMethods(test_cls: Type[T]) -> str:
    names = []
    for name, value in test_cls.__dict__.items():
        if hasattr(value, '_is_test_method') and value._is_test_method:
            names.append(name)
    return ' '.join(names)


def Test(test_method: Callable[P, None]) -> Callable[P, None]:
    setattr(test_method, '_is_test_method', True)
    return test_method


def TestClass(test_cls: Type[T]) -> Type[T]:
    if hasattr(test_cls, 'testNames'):
        raise InvalidAttributeException(
            "Class decorated with @TestClass cannot contain 'testName' attribute"
        )
    
    test_cls.testNames = getTestMethods(test_cls)
    return test_cls
