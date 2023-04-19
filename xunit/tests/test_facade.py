from xunit.src import *
import xunit.src as xunit
from xunit.tests.testclasses import DummyTestCase


@TestClass
class TestFacade(TestCase):

    @Test
    def testFacadeWithTestClass(self) -> None:
        from xunit.tests.testclasses import MockPrint
        mock = MockPrint()
        mock("Test")
        assert mock.passed_value == "Test"
        xunit.run(
            subject=DummyTestCase,
            type="class",
            capture_output=mock
        )
        assert mock.passed_value == self.expectedValueForClass()

    def expectedValueForClass(self) -> str:
        result = TestResult()
        summary = MixedTestSummary(
        PassedSummary(passed_formatter=green),
        ErrorInfoSummary(failed_formatter=red, notCompleted_formatter=yellow),
        SimpleTestSummary()
        )
        suite = TestSuite.fromTestCase(DummyTestCase)
        suite.run(result)
        return summary.results(result)
