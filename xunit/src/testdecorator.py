from typing import Type, TypeVar, ParamSpec, Callable
from xunit.src.testcase import TestCase
from xunit.src.testexceptions import InvalidAttributeException

    
T = TypeVar('T', bound=TestCase)
P = ParamSpec('P')


def get_test_methods(test_cls: Type[T]) -> str:
    names = []
    for name, value in test_cls.__dict__.items():
        if hasattr(value, '_is_test_method') and value._is_test_method:
            names.append(name)
    return ' '.join(names)


def Test(test_method: Callable[P, None]) -> Callable[P, None]:
    setattr(test_method, '_is_test_method', True)
    return test_method


def TestClass(test_cls: Type[T]) -> Type[T]:
    if hasattr(test_cls, 'xunit_test_names'):
        raise InvalidAttributeException(
            "Class decorated with @TestClass cannot contain 'xunit_test_names' attribute"
        )
    
    test_cls.xunit_test_names = get_test_methods(test_cls)
    test_cls._is_xunit_test_class = True
    return test_cls
