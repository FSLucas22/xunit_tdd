from xunit import TestCase, WasRun, TestResult, TestSuite


class TestCaseTest(TestCase):
    test: WasRun

    def testTemplateMethod(self) -> None:
        self.test = WasRun("testMethod")
        self.test.run()
        assert self.test.log == "setUp testMethod tearDown"

    def testResult(self) -> None:
        test = WasRun("testMethod")
        result = test.run()
        assert "1 run, 0 failed" == result.summary()

    def testFailedResult(self) -> None:
        test = WasRun("testBrokenMethod")
        result = test.run()
        assert "1 run, 1 failed" == result.summary()

    def testSuite(self) -> None:
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        result = TestResult()
        suite.run(result)
        assert "2 run, 1 failed" == result.summary()


def main() -> None:
    print(TestCaseTest("testTemplateMethod").run().summary())
    print(TestCaseTest("testResult").run().summary())
    print(TestCaseTest("testFailedResult").run().summary())
    print(TestCaseTest("testSuite").run().summary())


if __name__ == "__main__":
    main()
