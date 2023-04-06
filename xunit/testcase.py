class TestResult:
    runCount: int
    failedCount: int
    notCompletedCount: int

    def __init__(self) -> None:
        self.runCount = 0
        self.failedCount = 0
        self.notCompletedCount = 0

    def testStarted(self) -> None:
        self.runCount += 1

    def testNotCompleted(self) -> None:
        self.notCompletedCount += 1

    def testFailed(self) -> None:
        self.failedCount += 1
        
    def summary(self) -> str:
        return f"{self.runCount} run, {self.failedCount} failed"


class TestCase:
    name: str
    
    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def run(self, result: TestResult) -> None:
        result.testStarted()
        try:
            self.setUp()
        except:
            result.testNotCompleted()
        try:
            method = getattr(self, self.name)
            method()
        except:
            result.testFailed()
        self.tearDown()


class TestSuite:
    tests: list[TestCase]

    def __init__(self) -> None:
        self.tests = []
        
    def add(self, test: TestCase) -> None:
        self.tests.append(test)

    def run(self, result: TestResult) -> None:
        for test in self.tests:
            test.run(result)
             

class WasRun(TestCase):
    log: str = ""
    
    def setUp(self) -> None:
        self.log = "setUp"

    def tearDown(self) -> None:
        self.log += " tearDown"

    def testMethod(self) -> None:
       self.log += " testMethod"

    def testBrokenMethod(self) -> None:
        raise Exception


class FailedSetUp(WasRun):
    def setUp(self) -> None:
        raise Exception
