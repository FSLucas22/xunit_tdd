from xunit.src.testresult import TestResult


class TestCase:
    name: str
    testNames: str

    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def run(self, result: TestResult) -> None:
        try:
            self.setUp()
            method = getattr(self, self.name)
        except:
            result.testNotCompleted(self.name)
            self.tearDown()
            return
        try:
            method()
            result.testPassed(self.name)
        except:
            result.testFailed(self.name)
        self.tearDown()
