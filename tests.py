from xunit import TestCase, WasRun, TestResult, TestSuite


class TestCaseTest(TestCase):
    test: WasRun

    def testTemplateMethod(self) -> None:
        result = TestResult()
        self.test = WasRun("testMethod")
        self.test.run(result)
        assert self.test.log == "setUp testMethod tearDown"

    def testResult(self) -> None:
        result = TestResult()
        test = WasRun("testMethod")
        test.run(result)
        assert "1 run, 0 failed" == result.summary()

    def testFailedResult(self) -> None:
        result = TestResult()
        test = WasRun("testBrokenMethod")
        test.run(result)
        assert "1 run, 1 failed" == result.summary()

    def testSuite(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        result = TestResult()
        suite.run(result)
        assert "2 run, 1 failed" == result.summary()


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
