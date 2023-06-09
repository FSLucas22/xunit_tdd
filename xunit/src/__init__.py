import importlib
from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import TestSuite as TestSuite
from xunit.src import testdecorator
from xunit.src.testexceptions import *
from xunit.src import testcolours
from xunit.src.factories import *
from xunit.src.formatters import *
from xunit.src.observer import *
import xunit.src.packagemanager  as pm
from typing import Type, Callable
from types import ModuleType


color = testcolours
Test = testdecorator.Test
TestClass = testdecorator.TestClass


DEFAULT_SUMMARY = MixedTestSummary(
    TestSummary(FORMATTERS),
    SimpleTestSummary())


DEFAULT_SUITE_FACTORY = NormalSuiteFactory()


class TestRunner(SubjectImp):
    capture_output: Callable[[str], None]
    summary: Summary
    suite_factory: SuiteFactory
    suite: TestSuite | None
    
    def __init__(self, capture_output: Callable[[str], None] = print, 
                 summary: Summary=DEFAULT_SUMMARY, 
                 suite_factory: SuiteFactory = DEFAULT_SUITE_FACTORY,
                 *observers: Observer,
                 suite: TestSuite | None = None) -> None:
        
        self.capture_output = capture_output
        self.summary = summary
        self.suite_factory = suite_factory
        self.suite = suite
        super().__init__(*observers)

    def run(self) -> None:
        result = TestResult()
        if self.suite is not None:
            self.suite.register(result.save_status)
            self.suite.run()
        self.capture_output(self.summary.results(result))

    def run_for_class(self, cls: Type[TestCase]) -> None:
        self.suite = self.suite_factory.from_test_case(cls, observers=[self.notify])
        self.run()

    def run_for_module(self, module: ModuleType) -> None:
        self.suite = self.suite_factory.from_module(module, observers=[self.notify])
        self.run()

    def run_for_package(
        self, package: ModuleType, ignore: pm.Predicate=pm.ignore_name
        ) -> None:
        self.suite = self.suite_factory.from_package(package, ignore, observers=[self.notify])
        self.run()
