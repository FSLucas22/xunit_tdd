from typing import Type, Self
from xunit.src.testcase import TestCase
from xunit.src.testresult import TestResult
from types import ModuleType
from inspect import getmembers, isfunction


class TestSuite:
    tests: list[TestCase]

    def __init__(self) -> None:
        self.tests = []
        
    def add(self, test: TestCase) -> None:
        self.tests.append(test)

    def run(self, result: TestResult) -> None:
        for test in self.tests:
            test.run(result)

    @classmethod
    def fromTestCase(cls, *tests: Type[TestCase]) -> Self:
        suite = cls()
        for testCase in tests:
            for testName in testCase.testNames.split():
                suite.add(testCase(testName))
        return suite

    @classmethod
    def fromModule(cls, *modules: ModuleType) -> Self:
        classes = []
        for module in modules:
            classes += getTestClasses(module)
        return cls.fromTestCase(*classes)


def getTestClasses(module: ModuleType) -> list[Type[TestCase]]:
    return [cls for _, cls in getmembers(
        module,
        lambda value: hasattr(value, "_is_xunit_test_class") and \
        value._is_xunit_test_class and value.__module__ == module.__name__
    )]
