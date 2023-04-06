from xunit import *


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
        assert 1 == self.result.runCount
        assert 0 == self.result.failedCount
        assert 0 == self.result.notCompletedCount

    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert 1 == self.result.runCount
        assert 1 == self.result.failedCount
        assert 0 == self.result.notCompletedCount
        
    def testFailedResultCallsTearDown(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert "tearDown" in test.log

    def testFailedInSetUp(self) -> None:
        test = FailedSetUp("testMethod")
        test.run(self.result)
        assert "tearDown" in test.log
        assert self.result.runCount == 0
        assert self.result.failedCount == 0
        assert self.result.notCompletedCount == 1

    def testSummary(self) -> None:
        summary = TestSummary()
        self.result.testStarted()
        self.result.testNotCompleted()
        assert summary.results(self.result) == "1 run, 0 failed, 1 not completed"

    def testSuite(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.run(self.result)
        assert self.result.runCount == 2
        assert self.result.failedCount == 1
        assert self.result.notCompletedCount == 0

    def testCompletedTests(self) -> None:
        assert self.result.getAllStarted() == ""
        self.result.testStarted("someTest")
        assert self.result.getAllStarted() == "someTest"
        self.result.testFailed("someTest")
        assert self.result.getAllStarted() == "someTest"
        assert self.result.getAllFailed() == "someTest"

    def testCompletedMultipleTests(self) -> None:
        self.result.testStarted("someTest")
        self.result.testStarted("someOtherTest")
        assert self.result.getAllStarted() == "someTest someOtherTest"
        


def main() -> None:
    result = TestResult()
    summary = TestSummary()
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
    suite.run(result)
    print(summary.results(result))


if __name__ == "__main__":
    main()
