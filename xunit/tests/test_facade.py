from xunit.src import *
from xunit.tests.testclasses import WasRun
from xunit.tests.testclasses import MockPrint


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
    def test_facade(self) -> None:
        suite = VerboseSuiteFactory().from_test_case(WasRun)

        self.runner.suite = suite
        self.runner.run()
        assert self.print.passed_value == self.expected_value(suite)

    def expected_value(self, suite: TestSuite) -> str:
        result = TestResult()
        suite.register(result.save_status)
        suite.run()
        return self.summary.results(result)
