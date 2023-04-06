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

    def testSuite(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.run(self.result)
        assert "2 run, 1 failed" == self.result.summary()


def main() -> None:
    result = TestResult()
    suite = TestSuite()
    suite.add(TestCaseTest("testTemplateMethod"))
    suite.add(TestCaseTest("testResult"))
    suite.add(TestCaseTest("testFailedResult"))
    suite.add(TestCaseTest("testFailedResultCallsTearDown"))
    suite.add(TestCaseTest("testSuite"))
    suite.add(TestCaseTest("testFailedInSetUp"))
    suite.run(result)
    print(result.summary())


if __name__ == "__main__":
    main()
