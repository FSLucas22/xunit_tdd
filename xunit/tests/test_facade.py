from xunit.src import *
from xunit.tests.testclasses import DummyTestCase
from xunit.tests import testmodule
from xunit.tests.testclasses import MockPrint
from xunit.tests import testpackage


@TestClass
class TestFacade(TestCase):

    print: MockPrint
    runner: TestRunner

    def setup(self) -> None:
        self.print = MockPrint()
        self.runner = TestRunner(self.print)

    @Test
    def test_mock(self) -> None:
        self.print("Test")
        assert self.print.passed_value == "Test"

    @Test
    def test_facade_with_test_class(self) -> None:
        self.runner.run_for_class(DummyTestCase)
        assert self.print.passed_value == self.expected_value_for_class()

    @Test
    def test_facade_with_module(self) -> None:
        self.runner.run_for_module(testmodule)
        assert self.print.passed_value == self.expected_value_for_module()

    @Test
    def test_facade_with_package(self) -> None:
        self.runner.run_for_package(
            testpackage, ignore=lambda obj, _: obj.name != "packagemodule"
        )
        assert self.print.passed_value == self.expected_value_for_package()

    @Test
    def test_facade_with_module_path(self) -> None:
        self.runner.run_for_module_path(testmodule.__file__)
        assert self.print.passed_value == self.expected_value_for_module()

    @Test
    def test_facade_with_package_path(self) -> None:
        self.runner.run_for_package_path(
            testpackage.__file__, ignore=lambda obj, _: obj.name != "packagemodule"
        )
        assert self.print.passed_value == self.expected_value_for_package()

    def expected_value_for_class(self) -> str:
        result = TestResult()
        summary = MixedTestSummary(
        PassedSummary(passed_formatter=color.green),
        ErrorInfoSummary(
            failed_formatter=color.red,
            not_completed_formatter=color.yellow
        ),
        SimpleTestSummary()
        )
        suite = TestSuite.from_test_case(DummyTestCase)
        suite.run(result)
        return summary.results(result)

    def expected_value_for_module(self) -> str:
        result = TestResult()
        summary = MixedTestSummary(
        PassedSummary(passed_formatter=color.green),
        ErrorInfoSummary(
            failed_formatter=color.red,
            not_completed_formatter=color.yellow
        ),
        SimpleTestSummary()
        )
        suite = TestSuite.from_module(testmodule)
        suite.run(result)
        return summary.results(result)

    def expected_value_for_package(self) -> str:
        result = TestResult()
        summary = MixedTestSummary(
        PassedSummary(passed_formatter=color.green),
        ErrorInfoSummary(
            failed_formatter=color.red,
            not_completed_formatter=color.yellow
        ),
        SimpleTestSummary()
        )
        suite = TestSuite.from_package(
            testpackage, ignore=lambda obj, _: obj.name != "packagemodule"
        )
        suite.run(result)
        return summary.results(result)
