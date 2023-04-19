from xunit.src import *
import xunit.src as xunit
from xunit.tests.testclasses import DummyTestCase
from xunit.tests import testmodule
from xunit.tests.testclasses import MockPrint
from xunit.tests import testpackage


@TestClass
class TestFacade(TestCase):

    print: MockPrint

    def setUp(self) -> None:
        self.print = MockPrint()

    @Test
    def testMock(self) -> None:
        self.print("Test")
        assert self.print.passed_value == "Test"

    @Test
    def testFacadeWithTestClass(self) -> None:
        xunit.run(
            subject=DummyTestCase,
            type="class",
            capture_output=self.print
        )
        assert self.print.passed_value == self.expectedValueForClass()

    @Test
    def testFacadeWithModule(self) -> None:
        xunit.run(
            subject=testmodule,
            type="module",
            capture_output=self.print
        )
        assert self.print.passed_value == self.expectedValueForModule()

    @Test
    def testFacadeWithPackage(self) -> None:
        xunit.run(
            subject=testpackage,
            type="package",
            capture_output=self.print
        )
        assert self.print.passed_value == self.expectedValueForPackage()

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

    def expectedValueForModule(self) -> str:
        result = TestResult()
        summary = MixedTestSummary(
        PassedSummary(passed_formatter=green),
        ErrorInfoSummary(failed_formatter=red, notCompleted_formatter=yellow),
        SimpleTestSummary()
        )
        suite = TestSuite.fromModule(testmodule)
        suite.run(result)
        return summary.results(result)

    def expectedValueForPackage(self) -> str:
        result = TestResult()
        summary = MixedTestSummary(
        PassedSummary(passed_formatter=green),
        ErrorInfoSummary(failed_formatter=red, notCompleted_formatter=yellow),
        SimpleTestSummary()
        )
        suite = TestSuite.fromPackage(testpackage)
        suite.run(result)
        return summary.results(result)
