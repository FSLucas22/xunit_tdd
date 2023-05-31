from xunit.src import *
from xunit.src.status import TestStatus
from xunit.src.observer import Subject
from xunit.src.testsuite import Runnable
from xunit.tests.testclasses import *
from xunit.src.packagemanager import ignore_name
from typing import Callable


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
        assert self.result.passed_count == 1
        assert self.result.failed_count == 1
        assert self.result.not_completed_count == 0
        assert "testMethod testBrokenMethod" == self.result.started
        assert "testMethod" == self.result.passed

    @Test
    def test_names_from_tests(self) -> None:
        assert DummyTestCase.xunit_test_names == "passedTest1 passedTest2 failedTest1 failedTest2"

    @Test
    def test_suite_from_multiple_test_cases(self) -> None:
        suite = TestSuite.from_test_case(DummyTestCase, DummyTestCase,
                                         observers=[self.result.save_status])
        suite.run()
        
        assert self.result.passed == "passedTest1 passedTest2 passedTest1 passedTest2"
        assert self.result.failed == "failedTest1 failedTest2 failedTest1 failedTest2"

    @Test
    def test_test_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.from_test_case(
            testmodule.SomeTest,
            testmodule.SomeOtherTest,
            observers=[self.result.save_status]
        )
        suite.run()
        assert self.result.passed == "someTest"
        assert self.result.failed == "someOtherTest"

    @Test
    def test_from_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.from_module(testmodule, testmodule, observers=[self.result.save_status])
        suite.run()
        assert self.result.passed == "someTest someTest"
        assert self.result.failed == "someOtherTest someOtherTest"

    @Test
    def test_from_package(self) -> None:
        import xunit.tests.testpackage as testpackage
        
        suite = TestSuite.from_package(testpackage, observers=[self.result.save_status])
        suite.run()

        assert "x" in self.result.passed and "y" in self.result.passed and "z" in self.result.passed
        assert "x1" in self.result.failed and "y1" in self.result.failed and "z1" in self.result.failed

    @Test
    def test_ignore(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackage"]
        suite = TestSuite.from_package(testpackage, ignore=ignore, observers=[self.result.save_status])
        suite.run()
        assert "y" == self.result.passed
        assert "y1" == self.result.failed

    @Test
    def test_ignore_perpetuates(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackagemodule"]
        suite = TestSuite.from_package(testpackage, ignore=ignore, observers=[self.result.save_status])
        suite.run()
        assert "y" == self.result.passed
        assert "y1" == self.result.failed

    @Test
    def test_can_ignore_names(self) -> None:
        import xunit.tests.testpackage as testpackage
        suite = TestSuite.from_package(testpackage, ignore_name, observers=[self.result.save_status])
        suite.run()
        passed = self.result.passed
        failed = self.result.failed
        assert "x" in passed and "y" in passed and "z" not in passed
        assert "x1" in failed and "y1" in failed and "z1" not in failed
        
    @Test
    def test_merge(self) -> None:
        suite1 = TestSuite.from_test_case(DummyTestCase)
        suite2 = TestSuite.from_test_case(DummyTestCase)
        
        merged = suite1.merge(suite2)
        
        merged.register(self.result.save_status)
        merged.run()
        
        assert "passedTest1 passedTest2 passedTest1 passedTest2" == self.result.passed
        assert "failedTest1 failedTest2 failedTest1 failedTest2" == self.result.failed

        
    @Test
    def test_can_construct_suite_from_package_path(self) -> None:
        from xunit.tests import testpackage
        result1 = TestResult()
        result2 = TestResult()
        
        suite1 = TestSuite.from_path(
            "testpackage", testpackage.__file__, is_package=True, observers=[result1.save_status]
        )
        suite2 = TestSuite.from_package(testpackage, observers=[result2.save_status])
        
        suite1.run()
        suite2.run()
        
        assert result1.passed == result2.passed
        assert result1.failed == result2.failed
        assert result1.not_completed == result2.not_completed

    @Test
    def test_can_construct_suite_from_module_path(self) -> None:
        from xunit.tests.testpackage.subpackage import subpackagemodule
        result1 = TestResult()
        result2 = TestResult()
        
        suite1 = TestSuite.from_path(
            "subpackagemodule", subpackagemodule.__file__, is_package=False, observers=[self.result.save_status]
        )
        suite2 = TestSuite.from_module(subpackagemodule, observers=[self.result.save_status])
        
        suite1.run()
        suite2.run()
        
        assert result1.passed == result2.passed
        assert result1.failed == result2.failed
        assert result1.not_completed == result2.not_completed

    @Test
    def test_can_inform_status(self) -> None:
        suite = TestSuite(self.result.save_status)
        suite.run()
        assert self.result.results == [TestStatus("Suite", Status.CREATED, "suite")]

    @Test
    def test_can_inform_error_in_run(self) -> None:
        @TestClass
        class TestCls(TestCase):
            @Test
            def test(self) -> None:
                pass
            
            def run(self) -> None:
                raise Exception()
        
        error_info_factory = lambda e, name, status: TestStatus(name, status, "error")

        suite = TestSuite.from_test_case(TestCls, observers=[self.result.save_status],
                                         error_info_factory=error_info_factory)
        suite.run()

        assert self.result.results == [
            TestStatus("Suite", Status.CREATED, "suite"),
            TestStatus("Suite", Status.CREATED, TestCls.__name__),
            TestStatus(TestCls.__name__, Status.FAILED_TO_RUN, "error")]









        

