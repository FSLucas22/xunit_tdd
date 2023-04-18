from typing import Type, Self
from xunit.src.testcase import TestCase
from xunit.src.testresult import TestResult
from xunit.src.packagemanager import getPackageObjects, PackageObject, Predicate
from types import ModuleType
from inspect import getmembers, isfunction


class TestSuite:
    tests: list[TestCase]

    def __init__(self) -> None:
        self.tests = []
        
    def add(self, *tests: TestCase) -> None:
        self.tests += list(tests)

    def merge(self, otherSuite: 'TestSuite') -> 'TestSuite':
        merged = TestSuite()
        merged.tests = self.tests + otherSuite.tests
        return merged

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

    @classmethod
    def fromPackage(cls, package: ModuleType,
                    ignore: Predicate = lambda _,__: False) -> 'TestSuite':
        objs = getPackageObjects(package, ignore)
        suite = TestSuite()
        for obj in objs:
            obj_suite = cls.fromPackage(
                obj.value, ignore
                ) if obj.is_package else cls.fromModule(obj.value)
            suite = suite.merge(obj_suite)
        return suite


def getTestClasses(module: ModuleType) -> list[Type[TestCase]]:
    return [cls for _, cls in getmembers(
        module,
        lambda value: hasattr(value, "_is_xunit_test_class") and \
        value._is_xunit_test_class and value.__module__ == module.__name__
    )]











