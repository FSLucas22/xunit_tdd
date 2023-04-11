from xunit import *


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


class TestCaseTest(TestCase):
    test: WasRun
    result: TestResult
    testNames = "testTemplateMethod testResult testFailedResult testFailedResultCallsTearDown testFailedInSetUp "\
                "testNotCompletedWhenNotFound testSummary testSuite testCompletedTests testCompletedMultipleTests "\
                "testNotCompletedTests testPassedTests testDetailedSummary testRunnedEqualsPassedPlusFailed testSuiteFromTestCase "\
                "testNamesFromTests"
    
    def setUp(self) -> None:
        self.result = TestResult()

    def testTemplateMethod(self) -> None:
        self.test = WasRun("testMethod")
        self.test.run(self.result)
        assert self.test.log == "setUp testMethod tearDown"

    def testResult(self) -> None:
        test = WasRun("testMethod")
        test.run(self.result)
        assert 1 == self.result.passedCount
        assert 0 == self.result.failedCount
        assert 0 == self.result.notCompletedCount
        assert "testMethod" == self.result.getAllPassed()

    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert 1 == self.result.failedCount
        assert 0 == self.result.notCompletedCount
        assert "testBrokenMethod" == self.result.getAllFailed()
        
    def testFailedResultCallsTearDown(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert "tearDown" in test.log

    def testFailedInSetUp(self) -> None:
        test = FailedSetUp("testMethod")
        test.run(self.result)
        assert "tearDown" in test.log
        assert self.result.failedCount == 0
        assert self.result.notCompletedCount == 1
        assert "testMethod" == self.result.getAllNotCompleted()

    def testNotCompletedWhenNotFound(self) -> None:
        test = WasRun("notImplementedTest")
        test.run(self.result)
        assert self.result.notCompletedCount == 1
        assert "notImplementedTest" == self.result.getAllNotCompleted()

    def testSummary(self) -> None:
        summary = TestSummary()
        self.result.testPassed("someTest")
        self.result.testNotCompleted("someTest")
        assert summary.results(self.result) == "1 run, 0 failed, 1 not completed"

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

    def testCompletedTests(self) -> None:
        assert self.result.getAllStarted() == ""
        self.result.testFailed("someTest")
        assert self.result.getAllStarted() == "someTest"
        assert self.result.getAllFailed() == "someTest"

    def testCompletedMultipleTests(self) -> None:
        self.result.testFailed("someTest")
        self.result.testFailed("someOtherTest")
        assert self.result.getAllFailed() == "someTest someOtherTest"

    def testNotCompletedTests(self) -> None:
        assert self.result.getAllNotCompleted() == ""
        self.result.testNotCompleted("someBrokenTest")
        assert self.result.getAllNotCompleted() == "someBrokenTest"
        assert self.result.getAllFailed() == self.result.getAllStarted() == ""
        self.result.testNotCompleted("someOtherBrokenTest")
        assert self.result.getAllNotCompleted() == "someBrokenTest someOtherBrokenTest"

    def testPassedTests(self) -> None:
        assert self.result.getAllPassed() == ""
        self.result.testPassed("someTest")
        self.result.testPassed("someOtherTest")
        assert self.result.getAllPassed() == "someTest someOtherTest"
        
    def testDetailedSummary(self) -> None:
        summary = DetailedTestSummary()
        self.result.testPassed("someOtherTest")
        self.result.testFailed("someTest")
        self.result.testNotCompleted("someBrokenTest")
        assert summary.results(self.result) == "someTest - Failed\nsomeOtherTest - Passed\nsomeBrokenTest - Not completed"

    def testRunnedEqualsPassedPlusFailed(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.add(FailedSetUp("testMethod"))
        suite.run(self.result)
        assert self.result.passedCount == 1
        assert self.result.failedCount == 1
        assert self.result.runCount == self.result.passedCount + self.result.failedCount
        assert self.result.getAllStarted() == 'testMethod testBrokenMethod'

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


def main() -> None:
    result = TestResult()
    summary = DetailedTestSummary()
    resumedSummary = TestSummary()
    suite = TestSuite.fromTestCase(TestCaseTest)
    suite.run(result)
    print(summary.results(result))
    print(resumedSummary.results(result))
    

if __name__ == "__main__":
    main()
