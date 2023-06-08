from xunit.src import *
from xunit.tests import testmodule
from xunit.tests.testclasses import WasRun
from xunit.tests.testclasses import MockPrint
from xunit.tests import testpackage


@TestClass
class TestFacade(TestCase):

    print: MockPrint
    runner: TestRunner
    summary: Summary

    def setup(self) -> None:
        self.print = MockPrint()
        self.summary = TestSummary()
        self.result = TestResult()
        self.runner = TestRunner(self.print, self.summary)

    @Test
    def test_mock(self) -> None:
        self.print("Test")
        assert self.print.passed_value == "Test"

    @Test
    def test_facade_with_test_class(self) -> None:
        suite = TestSuite.from_test_case(WasRun)

        self.runner.run_for_class(WasRun)
        assert self.print.passed_value == self.expected_value(suite)

    @Test
    def test_facade_with_module(self) -> None:
        suite = TestSuite.from_module(testmodule)

        self.runner.run_for_module(testmodule)
        assert self.print.passed_value == self.expected_value(suite)

    @Test
    def test_facade_with_package(self) -> None:
        suite = TestSuite.from_package(
            testpackage, ignore=lambda obj, _: obj.name != "packagemodule")
        
        self.runner.run_for_package(
            testpackage, ignore=lambda obj, _: obj.name != "packagemodule")
        
        assert self.print.passed_value == self.expected_value(suite)

    @Test
    def test_facade_with_module_path(self) -> None:
        suite = TestSuite.from_module(testmodule)

        self.runner.run_for_module_name(testmodule.__name__)
        assert self.print.passed_value == self.expected_value(suite)

    @Test
    def test_facade_with_package_path(self) -> None:
        suite = TestSuite.from_package(
            testpackage, ignore=lambda obj, _: obj.name != "packagemodule")
        
        self.runner.run_for_package_name(
            testpackage.__name__, ignore=lambda obj, _: obj.name != "packagemodule")
        
        assert self.print.passed_value == self.expected_value(suite)

    def expected_value(self, suite: TestSuite) -> str:
        result = TestResult()
        suite.register(result.save_status)
        suite.run()
        return self.summary.results(result)
