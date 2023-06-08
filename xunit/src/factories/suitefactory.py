from types import ModuleType
from typing import Protocol, Type

from xunit.src.observer import Observer
from xunit.src.status import StatusFactory, TestStatus
from xunit.src.testcase import TestCase
from xunit.src.testsuite import DEFAULT_SUITE_NAME, TestSuite
from xunit.src import packagemanager as pm


class SuiteFactory(Protocol):
    def suite(self, observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME, 
              error_info_factory: StatusFactory = TestStatus.from_exception) -> TestSuite:
        ...
    
    def from_test_case(self, *tests: Type[TestCase],
                       observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME,
                       error_info_factory: StatusFactory = TestStatus.from_exception) -> TestSuite:
        ...
    
    def from_module(self, *modules: ModuleType,
                    observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME) -> TestSuite:
        ...

    def from_package(self, package: ModuleType,
                    ignore: pm.Predicate = lambda _,__: False,
                    observers: list[Observer] | None = None, name: str = DEFAULT_SUITE_NAME) -> TestSuite:
        ...
