from xunit.src import *
from xunit.tests.testclasses import *
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
        assert self.result.passedCount == 1
        assert self.result.failedCount == 1
        assert self.result.notCompletedCount == 0
        assert "testMethod testBrokenMethod" == self.result.getAllStarted()
        assert "testMethod" == self.result.getAllPassed()

    @Test
    def testSuiteFromTestCase(self) -> None:
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
        
        suite = TestSuite.fromTestCase(DummyTestCase)
        suite.run(self.result)
        
        assert self.result.getAllPassed() == individualResult.getAllPassed() == "passedTest1 passedTest2"
        assert self.result.getAllFailed() == individualResult.getAllFailed() == "failedTest1 failedTest2"

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
        
        suite = TestSuite.fromTestCase(DummyTestCase, DummyTestCase)
        suite.run(self.result)
        
        assert self.result.getAllPassed() == individualResult.getAllPassed() == "passedTest1 passedTest2 passedTest1 passedTest2"
        assert self.result.getAllFailed() == individualResult.getAllFailed() == "failedTest1 failedTest2 failedTest1 failedTest2"

    @Test
    def testTestModule(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.fromTestCase(
            testmodule.SomeTest,
            testmodule.SomeOtherTest
        )
        suite.run(self.result)
        assert self.result.getAllPassed() == "someTest"
        assert self.result.getAllFailed() == "someOtherTest"

    @Test
    def testFromModule(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.fromModule(testmodule, testmodule)
        suite.run(self.result)
        assert self.result.getAllPassed() == "someTest someTest"
        assert self.result.getAllFailed() == "someOtherTest someOtherTest"

    @Test
    def testFromPackage(self) -> None:
        from xunit.tests.testpackage import (
            packagemodule, packagemodule2, subpackage
        )
        from xunit.tests.testpackage.subpackage import subpackagemodule
        import xunit.tests.testpackage as testpackage
        suite = TestSuite.fromModule(packagemodule, packagemodule2, subpackagemodule)
        packagesuite = TestSuite.fromPackage(testpackage)
        result = TestResult()
        packagesuite.run(result)
        suite.run(self.result)
        assert self.result.getAllPassed() == "x y z" == result.getAllPassed()
        assert self.result.getAllFailed() == "x1 y1 z1" == result.getAllFailed()
        
    @Test
    def testMerge(self) -> None:
        suite1 = TestSuite.fromTestCase(DummyTestCase)
        suite2 = TestSuite.fromTestCase(DummyTestCase)
        merged = suite1.merge(suite2)
        result1 = TestResult()
        result2 = TestResult()
        mergedResult = TestResult()
        suite1.run(result1)
        suite2.run(result2)
        merged.run(mergedResult)

        assert result1.getAllPassed() == result2.getAllPassed() == "passedTest1 passedTest2"
        assert result1.getAllFailed() == result2.getAllFailed() == "failedTest1 failedTest2"
        assert result1.getAllPassed() + " " + result2.getAllPassed() == mergedResult.getAllPassed()
        assert result1.getAllFailed() + " " + result2.getAllFailed() == mergedResult.getAllFailed()

        
        


