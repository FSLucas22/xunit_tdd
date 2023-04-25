from xunit.src import *
from xunit.src.status import TestStatus
from xunit.src.observer import Subject
from xunit.tests.testclasses import *
from xunit.src.packagemanager import ignore_name
from importlib import import_module


@TestClass
class TestSuiteTest(TestCase):
    result: TestResult
    
    def setup(self) -> None:
        self.result = TestResult()

    @Test
    def test_suite(self) -> None:
        suite = TestSuite()
        suite.register(self.result.save_status)
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
        individual_result = TestResult()
        
        normal_suite = TestSuite()
        normal_suite.register(individual_result.save_status)
        normal_suite.add(
            DummyTestCase("passedTest1"),
            DummyTestCase("passedTest2"),
            DummyTestCase("failedTest1"),
            DummyTestCase("failedTest2"),
            DummyTestCase("passedTest1"),
            DummyTestCase("passedTest2"),
            DummyTestCase("failedTest1"),
            DummyTestCase("failedTest2")
        )
        normal_suite.run(TestResult())
        
        suite = TestSuite.from_test_case(DummyTestCase, DummyTestCase)
        suite.register(self.result.save_status)
        suite.run(TestResult())
        
        assert self.result.passed == individual_result.passed == "passedTest1 passedTest2" \
                                                               " passedTest1 passedTest2"
        assert self.result.failed == individual_result.failed == "failedTest1 failedTest2" \
                                                               " failedTest1 failedTest2"

    @Test
    def test_test_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.from_test_case(
            testmodule.SomeTest,
            testmodule.SomeOtherTest
        )
        suite.register(self.result.save_status)
        suite.run(TestResult())
        assert self.result.passed == "someTest"
        assert self.result.failed == "someOtherTest"

    @Test
    def test_from_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.from_module(testmodule, testmodule)
        suite.register(self.result.save_status)
        suite.run(TestResult())
        assert self.result.passed == "someTest someTest"
        assert self.result.failed == "someOtherTest someOtherTest"

    @Test
    def test_from_package(self) -> None:
        from xunit.tests.testpackage import (
            packagemodule, packagemodule2, subpackage
        )
        from xunit.tests.testpackage.subpackage import subpackagemodule
        import xunit.tests.testpackage as testpackage
        
        suite = TestSuite.from_module(packagemodule, packagemodule2, subpackagemodule)
        suite.register(self.result.save_status)
        packagesuite = TestSuite.from_package(testpackage)
        result = TestResult()
        packagesuite.register(result.save_status)
        
        packagesuite.run(TestResult())
        suite.run(TestResult())
        
        normal_passed = self.result.passed
        normal_failed = self.result.failed
        package_passed = result.passed
        package_failed = result.failed
        
        assert "x" in normal_passed and "y" in normal_passed and "z" in normal_passed
        assert "x" in package_passed and "y" in package_passed and "z" in package_passed
        assert "x1" in normal_failed and "y1" in normal_failed and "z1" in normal_failed
        assert "x1" in package_failed and "y1" in package_failed and "z1" in package_failed

    @Test
    def test_ignore(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackage"]
        suite = TestSuite.from_package(testpackage, ignore=ignore)
        suite.register(self.result.save_status)
        suite.run(TestResult())
        assert "y" == self.result.passed
        assert "y1" == self.result.failed

    @Test
    def test_ignore_perpetuates(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackagemodule"]
        suite = TestSuite.from_package(testpackage, ignore=ignore)
        suite.register(self.result.save_status)
        suite.run(TestResult())
        assert "y" == self.result.passed
        assert "y1" == self.result.failed

    @Test
    def test_can_ignore_names(self) -> None:
        import xunit.tests.testpackage as testpackage
        suite = TestSuite.from_package(testpackage, ignore_name)
        suite.register(self.result.save_status)
        suite.run(TestResult())
        passed = self.result.passed
        failed = self.result.failed
        assert "x" in passed and "y" in passed and "z" not in passed
        assert "x1" in failed and "y1" in failed and "z1" not in failed
        
    @Test
    def test_merge(self) -> None:
        suite1 = TestSuite.from_test_case(DummyTestCase)
        result1 = TestResult()
        suite1.register(result1.save_status)
        suite1.run(TestResult())
        
        suite2 = TestSuite.from_test_case(DummyTestCase)
        result2 = TestResult()
        suite2.register(result2.save_status)
        suite2.run(TestResult())

        merged = suite1.merge(suite2)
        
        suite1.unregister(result1.save_status)
        suite2.unregister(result2.save_status)

        merged_result = TestResult()
        merged.register(merged_result.save_status)
        merged.run(TestResult())
        
        assert result1.passed == result2.passed == "passedTest1 passedTest2"
        assert result1.failed == result2.failed == "failedTest1 failedTest2"
        assert result1.passed + " " + result2.passed == merged_result.passed
        assert result1.failed + " " + result2.failed == merged_result.failed

        
    @Test
    def test_can_construct_suite_from_package_path(self) -> None:
        from xunit.tests import testpackage
        suite1 = TestSuite.from_path(
            "testpackage", testpackage.__file__, is_package=True
        )
        suite2 = TestSuite.from_package(testpackage)
        result1 = TestResult()
        result2 = TestResult()

        suite1.register(result1.save_status)
        suite2.register(result2.save_status)
        
        suite1.run(TestResult())
        suite2.run(TestResult())
        
        assert result1.passed == result2.passed
        assert result1.failed == result2.failed
        assert result1.not_completed == result2.not_completed

    @Test
    def test_can_construct_suite_from_module_path(self) -> None:
        from xunit.tests.testpackage.subpackage import subpackagemodule
        suite1 = TestSuite.from_path(
            "subpackagemodule", subpackagemodule.__file__, is_package=False
        )
        suite2 = TestSuite.from_module(subpackagemodule)
        result1 = TestResult()
        result2 = TestResult()

        suite1.register(result1.save_status)
        suite2.register(result2.save_status)
        
        suite1.run(TestResult())
        suite2.run(TestResult())
        
        assert result1.passed == result2.passed
        assert result1.failed == result2.failed
        assert result1.not_completed == result2.not_completed

    @Test
    def test_testsuite_is_subject(self) -> None:
        subject: Subject = TestSuite() 
        observer1 = DummyObserver()
        observer2 = DummyObserver()
        status = TestStatus("x", "y", "z")
        subject.register(observer1, observer2)
        subject.notify(status)
        assert observer1.received == observer2.received == [status]
        subject.unregister(observer1)
        subject.notify(status)
        assert observer1.received == [status]
        assert observer2.received == [status, status]

