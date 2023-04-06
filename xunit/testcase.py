class TestResult:
    runCount: int
    failedCount: int
    notCompletedCount: int
    runned: str
    failed: str

    def __init__(self) -> None:
        self.runCount = 0
        self.failedCount = 0
        self.notCompletedCount = 0
        self.runned = ""
        self.failed = ""

    def testStarted(self, test_name: str = "AnonTest") -> None:
        self.runCount += 1
        self.runned += test_name

    def testNotCompleted(self) -> None:
        self.notCompletedCount += 1

    def testFailed(self, test_name: str = "AnonTest") -> None:
        self.failedCount += 1
        self.failed += test_name

    def getAllStarted(self) -> str:
        return self.runned

    def getAllFailed(self) -> str:
        return self.failed


class TestSummary:
    def results(self, result: TestResult) -> str:
        return f"{result.runCount} run, {result.failedCount} failed, {result.notCompletedCount} not completed"


class TestCase:
    name: str
    
    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def run(self, result: TestResult) -> None:
        try:
            self.setUp()
        except:
            result.testNotCompleted()
            self.tearDown()
            return
        try:
            result.testStarted()
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
