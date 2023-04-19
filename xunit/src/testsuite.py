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

    def merge(self, other_suite: 'TestSuite') -> 'TestSuite':
        merged = TestSuite()
        merged._tests = self._tests + other_suite._tests
        return merged

    def run(self, result: TestResult) -> None:
        for test in self._tests:
            test.run(result)

    @classmethod
    def from_test_case(cls, *tests: Type[TestCase]) -> Self:
        suite = cls()
        for test_case in tests:
            for testName in test_case.testNames.split():
                suite.add(test_case(testName))
        return suite

    @classmethod
    def from_module(cls, *modules: ModuleType) -> Self:
        classes = []
        for module in modules:
            classes += getTestClasses(module)
        return cls.from_test_case(*classes)

    @classmethod
    def from_package(cls, package: ModuleType,
                    ignore: Predicate = lambda _,__: False) -> 'TestSuite':
        objs = getPackageObjects(package, ignore)
        suite = TestSuite()
        for obj in objs:
            obj_suite = cls.from_package(
                obj.value, ignore
                ) if obj.is_package else cls.from_module(obj.value)
            suite = suite.merge(obj_suite)
        return suite

    @classmethod
    def from_path(cls, name: str, path: str, is_package: bool,
                 ignore: Predicate=lambda _,__: False) -> 'TestSuite':
        module = findModule(name, path)
        if is_package:
            return cls.from_package(module, ignore)
        return cls.from_module(module)











