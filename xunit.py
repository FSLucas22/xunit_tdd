class TestResult:
    runCount: int

    def __init__(self) -> None:
        self.runCount = 0

    def testStarted(self) -> None:
        self.runCount += 1

    def testFailed(self) -> None:
        pass
        
    def summary(self) -> str:
        return f"{self.runCount} run, 0 failed"


class TestCase:
    name: str
    
    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def run(self) -> TestResult:
        result = TestResult()
        result.testStarted()
        self.setUp()
        method = getattr(self, self.name)
        method()
        self.tearDown()
        return result
        

class WasRun(TestCase):
    wasRun: int | None
    log: str
    
    def setUp(self) -> None:
        self.wasRun = None
        self.log = "setUp"

    def tearDown(self) -> None:
        self.log += " tearDown"

    def testMethod(self) -> None:
       self.wasRun = 1
       self.log += " testMethod"

    def testBrokenMethod(self) -> None:
        raise Exception


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

    def testFailedResultFormatting(self) -> None:
        result = TestResult()
        result.testStarted()
        result.testFailed()
        assert "1 run, 1 failed" == result.summary()


def main() -> None:
    TestCaseTest("testTemplateMethod").run()
    TestCaseTest("testResult").run()
    TestCaseTest("testFailedResultFormatting").run()
    # TestCaseTest("testFailedResult").run()


if __name__ == "__main__":
    main()
