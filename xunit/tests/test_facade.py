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
    suite_factory: SuiteFactory

    def setup(self) -> None:
        self.print = MockPrint()
        self.summary = TestSummary()
        self.result = TestResult()
        self.suite_factory = VerboseSuiteFactory()
        self.runner = TestRunner(self.print, self.summary, self.suite_factory)

    @Test
    def test_mock(self) -> None:
        self.print("Test")
        assert self.print.passed_value == "Test"

    @Test
    def test_facade_with_test_class(self) -> None:
        suite = self.suite_factory.from_test_case(WasRun)

        self.runner.run_for_class(WasRun)
        assert self.print.passed_value == self.expected_value(suite)

    @Test
    def test_facade_with_module(self) -> None:
        suite = self.suite_factory.from_module(testmodule)

        self.runner.run_for_module(testmodule)
        assert self.print.passed_value == self.expected_value(suite)

    @Test
    def test_facade_with_package(self) -> None:
        suite = self.suite_factory.from_package(
            testpackage, ignore=lambda obj, _: obj.name != "packagemodule")
        
        self.runner.run_for_package(
            testpackage, ignore=lambda obj, _: obj.name != "packagemodule")
        
        assert self.print.passed_value == self.expected_value(suite)

    def expected_value(self, suite: TestSuite) -> str:
        result = TestResult()
        suite.register(result.save_status)
        suite.run()
        return self.summary.results(result)
