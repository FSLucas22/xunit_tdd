from typing import Type, Callable, TypeVar
from xunit.src.testcase import TestCase


TestSubCase = TypeVar('TestSubCase', bound=TestCase)
TestMethod = Callable[[TestSubCase], None]

def Test(test_cls: Type[TestCase]
         ) -> Callable[[TestMethod[TestSubCase]], TestMethod[TestSubCase]]:
    def getMethod(test_method: TestMethod[TestSubCase]
                  ) -> TestMethod[TestSubCase]:
        test_name = test_method.__name__
        if not hasattr(test_cls, 'testNames') or test_cls.testNames == "":
            test_cls.testNames = test_name
            return test_method
        test_cls.testNames += " " + test_name
        return test_method
    return getMethod
