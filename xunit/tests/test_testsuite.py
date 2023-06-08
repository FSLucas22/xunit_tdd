from xunit.src import *
from xunit.src.status import TestStatus
from xunit.tests.testclasses import *
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
        assert "testMethod" == self.result.get_names_of_status(Status.PASSED)

    @Test
    def test_suite_from_multiple_test_cases(self) -> None:
        TestSuite.from_test_case(
            PassedTestCase, FailedTestCase,
            observers=[self.result.save_status]).run()
  
        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "passed_test failed_test"

    @Test
    def test_test_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.from_test_case(
            testmodule.SomeTest,
            testmodule.SomeOtherTest,
            observers=[self.result.save_status]
        )
        suite.run()
        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "someTest someOtherTest"

    @Test
    def test_from_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.from_module(testmodule, testmodule, observers=[self.result.save_status])
        suite.run()
        assert self.result.get_names_of_status(
            Status.PASSED, Status.FAILED) == "someTest someTest someOtherTest someOtherTest"

    @Test
    def test_from_package(self) -> None:
        import xunit.tests.testpackage as testpackage
        
        suite = TestSuite.from_package(testpackage, observers=[self.result.save_status])
        suite.run()
        passed = self.result.get_names_of_status(Status.PASSED)
        failed = self.result.get_names_of_status(Status.FAILED)
        assert "x" in passed and "y" in passed and "z" in passed
        assert "x1" in failed and "y1" in failed and "z1" in failed

    @Test
    def test_ignore(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackage"]
        suite = TestSuite.from_package(testpackage, ignore=ignore, observers=[self.result.save_status])
        suite.run()
        assert "y y1" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)

    @Test
    def test_ignore_perpetuates(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackagemodule"]
        suite = TestSuite.from_package(testpackage, ignore=ignore, observers=[self.result.save_status])
        suite.run()
        assert "y y1" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)

    @Test
    def test_merge(self) -> None:
        suite1 = TestSuite.from_test_case(PassedTestCase)
        suite2 = TestSuite.from_test_case(FailedTestCase)
        
        merged = suite1.merge(suite2)
        
        merged.register(self.result.save_status)
        merged.run()
        
        assert "passed_test failed_test" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)

    @Test
    def test_can_inform_status(self) -> None:
        suite = TestSuite(self.result.save_status)
        suite.run()
        assert self.result.get_results() == [TestStatus("Suite", Status.CREATED, "suite")]

    @Test
    def test_can_inform_error_in_run(self) -> None:
        error_info_factory = cast(StatusFactory, lambda e, name, status: TestStatus(name, status, "error"))

        suite = TestSuite.from_test_case(UnrunnableTest, observers=[self.result.save_status],
                                         error_info_factory=error_info_factory)
        suite.run()

        assert self.result.get_results() == [
            TestStatus("Suite", Status.CREATED, "suite"),
            TestStatus("Suite", Status.CREATED, UnrunnableTest.__name__),
            TestStatus(UnrunnableTest.__name__, Status.FAILED_TO_RUN, "error")]
