from xunit.src import *
from xunit.tests.testclasses import *
from xunit.src.packagemanager import ignore_name
from importlib import import_module


@TestClass
class TestSuiteTest(TestCase):
    result: TestResult
    
    def setUp(self) -> None:
        self.result = TestResult()

    @Test
    def testSuite(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"), WasRun("testBrokenMethod"))
        suite.run(self.result)
        assert self.result.passed_count == 1
        assert self.result.failed_count == 1
        assert self.result.not_completed_count == 0
        assert "testMethod testBrokenMethod" == self.result.started
        assert "testMethod" == self.result.passed

    @Test
    def testSuitefrom_test_case(self) -> None:
        individualResult = TestResult()
        assert hasattr(DummyTestCase, "passedTest1")
        assert hasattr(DummyTestCase, "passedTest2")
        assert hasattr(DummyTestCase, "failedTest1")
        assert hasattr(DummyTestCase, "failedTest2")
        
        normalSuite = TestSuite()
        normalSuite.add(
            DummyTestCase("passedTest1"),
            DummyTestCase("passedTest2"),
            DummyTestCase("failedTest1"),
            DummyTestCase("failedTest2")
        )
        normalSuite.run(individualResult)
        
        suite = TestSuite.from_test_case(DummyTestCase)
        suite.run(self.result)
        
        assert self.result.passed == individualResult.passed == "passedTest1 passedTest2"
        assert self.result.failed == individualResult.failed == "failedTest1 failedTest2"

    @Test
    def testNamesFromTests(self) -> None:
        assert DummyTestCase.testNames == "passedTest1 passedTest2 failedTest1 failedTest2"

    @Test
    def testSuiteFromMultipleTestCases(self) -> None:
        individualResult = TestResult()
        
        normalSuite = TestSuite()
        normalSuite.add(
            DummyTestCase("passedTest1"),
            DummyTestCase("passedTest2"),
            DummyTestCase("failedTest1"),
            DummyTestCase("failedTest2"),
            DummyTestCase("passedTest1"),
            DummyTestCase("passedTest2"),
            DummyTestCase("failedTest1"),
            DummyTestCase("failedTest2")
        )
        normalSuite.run(individualResult)
        
        suite = TestSuite.from_test_case(DummyTestCase, DummyTestCase)
        suite.run(self.result)
        
        assert self.result.passed == individualResult.passed == "passedTest1 passedTest2 passedTest1 passedTest2"
        assert self.result.failed == individualResult.failed == "failedTest1 failedTest2 failedTest1 failedTest2"

    @Test
    def testTestModule(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.from_test_case(
            testmodule.SomeTest,
            testmodule.SomeOtherTest
        )
        suite.run(self.result)
        assert self.result.passed == "someTest"
        assert self.result.failed == "someOtherTest"

    @Test
    def testfrom_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.from_module(testmodule, testmodule)
        suite.run(self.result)
        assert self.result.passed == "someTest someTest"
        assert self.result.failed == "someOtherTest someOtherTest"

    @Test
    def testfrom_package(self) -> None:
        from xunit.tests.testpackage import (
            packagemodule, packagemodule2, subpackage
        )
        from xunit.tests.testpackage.subpackage import subpackagemodule
        import xunit.tests.testpackage as testpackage
        suite = TestSuite.from_module(packagemodule, packagemodule2, subpackagemodule)
        packagesuite = TestSuite.from_package(testpackage)
        result = TestResult()
        packagesuite.run(result)
        suite.run(self.result)
        normal_passed = self.result.passed
        normal_failed = self.result.failed
        package_passed = result.passed
        package_failed = result.failed
        
        assert "x" in normal_passed and "y" in normal_passed and "z" in normal_passed
        assert "x" in package_passed and "y" in package_passed and "z" in package_passed
        assert "x1" in normal_failed and "y1" in normal_failed and "z1" in normal_failed
        assert "x1" in package_failed and "y1" in package_failed and "z1" in package_failed

    @Test
    def testIgnore(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackage"]
        suite = TestSuite.from_package(testpackage, ignore=ignore)
        suite.run(self.result)
        assert "y" == self.result.passed
        assert "y1" == self.result.failed

    @Test
    def testIgnorePerpetuates(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackagemodule"]
        suite = TestSuite.from_package(testpackage, ignore=ignore)
        suite.run(self.result)
        assert "y" == self.result.passed
        assert "y1" == self.result.failed

    @Test
    def testCanIgnoreNames(self) -> None:
        import xunit.tests.testpackage as testpackage
        suite = TestSuite.from_package(testpackage, ignore_name)
        suite.run(self.result)
        passed = self.result.passed
        failed = self.result.failed
        assert "x" in passed and "y" in passed and "z" not in passed
        assert "x1" in failed and "y1" in failed and "z1" not in failed
        
    @Test
    def testMerge(self) -> None:
        suite1 = TestSuite.from_test_case(DummyTestCase)
        suite2 = TestSuite.from_test_case(DummyTestCase)
        merged = suite1.merge(suite2)
        result1 = TestResult()
        result2 = TestResult()
        mergedResult = TestResult()
        suite1.run(result1)
        suite2.run(result2)
        merged.run(mergedResult)

        assert result1.passed == result2.passed == "passedTest1 passedTest2"
        assert result1.failed == result2.failed == "failedTest1 failedTest2"
        assert result1.passed + " " + result2.passed == mergedResult.passed
        assert result1.failed + " " + result2.failed == mergedResult.failed

        
    @Test
    def testCanConstructASuitefrom_packagePath(self) -> None:
        from xunit.tests import testpackage
        suite1 = TestSuite.from_path(
            "testpackage", testpackage.__file__, is_package=True
        )
        suite2 = TestSuite.from_package(testpackage)
        result1 = TestResult()
        result2 = TestResult()
        suite1.run(result1)
        suite2.run(result2)
        assert result1.passed == result2.passed
        assert result1.failed == result2.failed
        assert result1.not_completed == result2.not_completed

    @Test
    def testCanConstructASuitefrom_modulePath(self) -> None:
        from xunit.tests.testpackage.subpackage import subpackagemodule
        suite1 = TestSuite.from_path(
            "subpackagemodule", subpackagemodule.__file__, is_package=False
        )
        suite2 = TestSuite.from_module(subpackagemodule)
        result1 = TestResult()
        result2 = TestResult()
        suite1.run(result1)
        suite2.run(result2)
        assert result1.passed == result2.passed
        assert result1.failed == result2.failed
        assert result1.not_completed == result2.not_completed        


