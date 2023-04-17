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
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
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
        normalSuite.add(DummyTestCase("passedTest1"))
        normalSuite.add(DummyTestCase("passedTest2"))
        normalSuite.add(DummyTestCase("failedTest1"))
        normalSuite.add(DummyTestCase("failedTest2"))
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
        normalSuite.add(DummyTestCase("passedTest1"))
        normalSuite.add(DummyTestCase("passedTest2"))
        normalSuite.add(DummyTestCase("failedTest1"))
        normalSuite.add(DummyTestCase("failedTest2"))
        normalSuite.add(DummyTestCase("passedTest1"))
        normalSuite.add(DummyTestCase("passedTest2"))
        normalSuite.add(DummyTestCase("failedTest1"))
        normalSuite.add(DummyTestCase("failedTest2"))
        normalSuite.run(individualResult)
        
        suite = TestSuite.fromTestCase(DummyTestCase, DummyTestCase)
        suite.run(self.result)
        
        assert self.result.getAllPassed() == individualResult.getAllPassed() == "passedTest1 passedTest2 passedTest1 passedTest2"
        assert self.result.getAllFailed() == individualResult.getAllFailed() == "failedTest1 failedTest2 failedTest1 failedTest2"

    @Test
    def testTestModule(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = TestSuite.fromTestCase(testmodule.SomeTest)
        suite.run(self.result)
        assert self.result.getAllPassed() == "someTest"

    @Test
    def testGetTestClasses(self) -> None:
        import xunit.tests.testmodule as testmodule
        classes = getTestClasses(testmodule)
        assert len(classes) == 2
        assert testmodule.SomeTest in classes
        assert testmodule.SomeOtherTest in classes
        
        


