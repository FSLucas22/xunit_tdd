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


class TestRunner:
    capture_output: Callable[[str], None]
    summary: Summary
    suite_factory: SuiteFactory

    def __init__(self, capture_output: Callable[[str], None] = print, 
                 summary: Summary=DEFAULT_SUMMARY, 
                 suite_factory: SuiteFactory = DEFAULT_SUITE_FACTORY) -> None:
        self.capture_output = capture_output
        self.summary = summary
        self.suite_factory = suite_factory

    def _run(self, suite: TestSuite) -> None:
        result = TestResult()
        suite.register(result.save_status)
        suite.run()
        self.capture_output(self.summary.results(result))

    def run_for_class(self, cls: Type[TestCase]) -> None:
        self._run(self.suite_factory.from_test_case(cls))

    def run_for_module(self, module: ModuleType) -> None:
        self._run(self.suite_factory.from_module(module))

    def run_for_package(
        self, package: ModuleType, ignore: pm.Predicate=pm.ignore_name
        ) -> None:
        self._run(self.suite_factory.from_package(package, ignore))
