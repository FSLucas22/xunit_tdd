from xunit.src import *
from xunit.tests.testclasses import DummyTestCase
from xunit.tests import testmodule
from xunit.tests.testclasses import MockPrint
from xunit.tests import testpackage


@TestClass
class TestFacade(TestCase):

    print: MockPrint
    runner: TestRunner
    summary: TestSummary
    result: TestResult

    def setup(self) -> None:
        self.print = MockPrint()
        self.summary = Summary({})
        self.result = TestResult()
        self.runner = TestRunner(self.print, Summary({}))

    @Test
    def test_mock(self) -> None:
        self.print("Test")
        assert self.print.passed_value == "Test"

    @Test
    def test_facade_with_test_class(self) -> None:
        suite = TestSuite.from_test_case(DummyTestCase)

        self.runner.run_for_class(DummyTestCase)
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

        self.runner.run_for_module_path(testmodule.__file__)
        assert self.print.passed_value == self.expected_value(suite)

    @Test
    def test_facade_with_package_path(self) -> None:
        suite = TestSuite.from_package(
            testpackage, ignore=lambda obj, _: obj.name != "packagemodule")
        
        self.runner.run_for_package_path(
            testpackage.__file__, ignore=lambda obj, _: obj.name != "packagemodule")
        
        assert self.print.passed_value == self.expected_value(suite)

    def expected_value(self, suite: TestSuite) -> str:
        suite.register(self.result.save_status)
        suite.run()
        return self.summary.results(self.result)
