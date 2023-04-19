from xunit.src import *
import xunit.src as xunit
from xunit.tests.testclasses import DummyTestCase
from xunit.tests import testmodule
from xunit.tests.testclasses import MockPrint
from xunit.tests import testpackage


@TestClass
class TestFacade(TestCase):

    print: MockPrint
    runner: TestRunner

    def setUp(self) -> None:
        self.print = MockPrint()
        self.runner = TestRunner(self.print)

    @Test
    def testMock(self) -> None:
        self.print("Test")
        assert self.print.passed_value == "Test"

    @Test
    def testFacadeWithTestClass(self) -> None:
        self.runner.runForClass(DummyTestCase)
        assert self.print.passed_value == self.expectedValueForClass()

    @Test
    def testFacadeWithModule(self) -> None:
        self.runner.runForModule(testmodule)
        assert self.print.passed_value == self.expectedValueForModule()

    @Test
    def testFacadeWithPackage(self) -> None:
        self.runner.runForPackage(testpackage)
        assert self.print.passed_value == self.expectedValueForPackage()

    @Test
    def testFacadeWithModulePath(self) -> None:
        self.runner.runForModulePath(testmodule.__file__)
        assert self.print.passed_value == self.expectedValueForModule()

    @Test
    def testFacadeWithPackagePath(self) -> None:
        self.runner.runForPackagePath(testpackage.__file__)
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
