from xunit import TestCase, WasRun, TestResult, TestSuite


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
        assert "1 run, 0 failed" == self.result.summary()

    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert "1 run, 1 failed" == self.result.summary()

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
    suite.add(TestCaseTest("testSuite"))
    suite.run(result)
    print(result.summary())


if __name__ == "__main__":
    main()
