from typing import Type, Self
from xunit.src.testcase import TestCase
from xunit.src.testresult import TestResult
from xunit.src.packagemanager import (
    getPackageObjects, PackageObject, Predicate, findModule, getTestClasses
)
from types import ModuleType


class TestSuite:
    
    def __init__(self) -> None:
        self._tests: list[TestCase] = []
        
    def add(self, *tests: TestCase) -> None:
        self._tests += list(tests)

    def merge(self, otherSuite: 'TestSuite') -> 'TestSuite':
        merged = TestSuite()
        merged._tests = self._tests + otherSuite._tests
        return merged

    def run(self, result: TestResult) -> None:
        for test in self._tests:
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

    @classmethod
    def fromPath(cls, name: str, path: str, is_package: bool,
                 ignore: Predicate=lambda _,__: False) -> 'TestSuite':
        module = findModule(name, path)
        if is_package:
            return cls.fromPackage(module, ignore)
        return cls.fromModule(module)











