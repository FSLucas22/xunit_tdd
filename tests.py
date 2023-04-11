from xunit import *


class DummyTestCase(TestCase):
    pass


class TestCaseTest(TestCase):
    test: WasRun
    result: TestResult
    
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
        suite = TestSuite.fromTestCase(DummyTestCase)
        suite.run(self.result)
        assert self.result.getAllPassed() == "testPassed1"


def main() -> None:
    result = TestResult()
    summary = DetailedTestSummary()
    resumedSummary = TestSummary()
    suite = TestSuite()
    suite.add(TestCaseTest("testTemplateMethod"))
    suite.add(TestCaseTest("testResult"))
    suite.add(TestCaseTest("testFailedResult"))
    suite.add(TestCaseTest("testFailedResultCallsTearDown"))
    suite.add(TestCaseTest("testSuite"))
    suite.add(TestCaseTest("testFailedInSetUp"))
    suite.add(TestCaseTest("testSummary"))
    suite.add(TestCaseTest("testCompletedTests"))
    suite.add(TestCaseTest("testCompletedMultipleTests"))
    suite.add(TestCaseTest("testNotCompletedTests"))
    suite.add(TestCaseTest("testPassedTests"))
    suite.add(TestCaseTest("testDetailedSummary"))
    suite.add(TestCaseTest("testRunnedEqualsPassedPlusFailed"))
    suite.add(TestCaseTest("testNotCompletedWhenNotFound"))
    suite.add(TestCaseTest("testSuiteFromTestCase"))
    suite.run(result)
    print(summary.results(result))
    print(resumedSummary.results(result))
    

if __name__ == "__main__":
    main()
