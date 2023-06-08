from types import ModuleType
from typing import Type

from xunit.src.observer import Observer
from xunit.src.status import StatusFactory, TestStatus
from xunit.src.testcase import TestCase
from xunit.src.testsuite import DEFAULT_SUITE_NAME, TestSuite
from xunit.src import packagemanager as pm


class NormalSuiteFactory:
    def suite(self, observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME,
              error_info_factory: StatusFactory = TestStatus.from_exception) -> TestSuite:
        if observers is None:
            observers = []
        return TestSuite(*observers, name=name, error_info_factory=error_info_factory)

    def from_test_case(self, *tests: Type[TestCase],
                       observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME,
                       error_info_factory: StatusFactory = TestStatus.from_exception) -> TestSuite:
        suite = self.suite(observers, name, error_info_factory)
        for test_case in tests:
            test_suite = self.suite(name=test_case.__name__, error_info_factory=error_info_factory)
            for testname in test_case.xunit_test_names.split():
                test_suite.add(test_case(testname))
            suite.add(test_suite)
        return suite

    def from_module(self, *modules: ModuleType,
                    observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME) -> TestSuite:
        base_suite = self.suite(observers=observers, name=name)
        for module in modules:
            module_suite = self.from_test_case(*pm.get_test_classes(module), name=module.__name__)
            base_suite.add(*module_suite._tests)
        return base_suite

    def from_package(self, package: ModuleType,
                    ignore: pm.Predicate = lambda _,__: False,
                    observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME) -> TestSuite:
        objs = pm.get_package_objects(package, ignore)
        suite = self.suite(name=name)
        for obj in objs:
            obj_suite = self.from_package(
                obj.value, ignore=ignore, name=obj.name
                ) if obj.is_package else self.from_module(obj.value, name=obj.name)
            suite.add(*obj_suite._tests)
        if observers is None:
            observers = []
        suite.register(*observers)
        return suite
