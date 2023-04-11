from xunit.src import *


class DummyTestCase(TestCase):
    testNames = "passedTest1 passedTest2 failedTest1 failedTest2"
    
    def passedTest1(self) -> None:
        pass

    def passedTest2(self) -> None:
        pass

    def failedTest1(self) -> None:
        raise Exception

    def failedTest2(self) -> None:
        raise Exception


class TestSuiteTest(TestCase):
    result: TestResult
    testNames = "testSuite testSuiteFromTestCase testNamesFromTests" 
    def setUp(self) -> None:
        self.result = TestResult()
        
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

    def testNamesFromTests(self) -> None:
        assert DummyTestCase.testNames == "passedTest1 passedTest2 failedTest1 failedTest2"
