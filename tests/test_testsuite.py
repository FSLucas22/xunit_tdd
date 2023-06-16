from src.xunit import *
from src.xunit.status import TestStatus
from src.xunit.testsuite import DEFAULT_SUITE_NAME
from .testclasses import *
from typing import cast


@TestClass
class TestSuiteTest(TestCase):
    result: TestResult
    
    def setup(self) -> None:
        self.result = TestResult()

    @Test
    def test_suite(self) -> None:
        suite = TestSuite(self.result.save_status)
        suite.add(WasRun("testMethod"), WasRun("testBrokenMethod"))
        suite.run()
        assert self.result.get_status_count(Status.PASSED) == 1
        assert self.result.get_status_count(Status.FAILED) == 1
        assert self.result.get_status_count(Status.NOT_COMPLETED) == 0
        assert "testMethod testBrokenMethod" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)

    @Test
    def test_can_inform_status(self) -> None:
        suite = TestSuite(self.result.save_status)
        suite.run()
        assert self.result.get_results() == [TestStatus("Suite", Status.CREATED, DEFAULT_SUITE_NAME)]

    @Test
    def test_can_inform_error_in_run(self) -> None:
        error_info_factory = cast(StatusFactory, lambda e, name, status: TestStatus(name, status, "error"))
        suite = TestSuite(self.result.save_status, error_info_factory=error_info_factory)

        suite.add(UnrunnableTest("test"))
        
        suite.run()

        assert self.result.get_results() == [
            TestStatus("Suite", Status.CREATED, DEFAULT_SUITE_NAME),
            TestStatus(UnrunnableTest.__name__, Status.FAILED_TO_RUN, "error")]
