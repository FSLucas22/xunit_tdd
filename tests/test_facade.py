from src.xunit import *
from .testclasses import WasRun
from .testclasses import MockPrint
from src.xunit import loader


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
        suite = loader.load(TestSuite(), loader.tests_from_class(WasRun))

        self.runner.runnable = suite
        self.runner.run()
        assert self.print.passed_value == self.expected_value(suite)

    def expected_value(self, suite: TestSuite) -> str:
        result = TestResult()
        suite.register(result.save_status)
        suite.run()
        return self.summary.results(result)
