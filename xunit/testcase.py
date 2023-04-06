class TestResult:
    runCount: int
    failedCount: int

    def __init__(self) -> None:
        self.runCount = 0
        self.failedCount = 0

    def testStarted(self) -> None:
        self.runCount += 1

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

    def run(self) -> TestResult:
        result = TestResult()
        result.testStarted()
        self.setUp()
        try:
            method = getattr(self, self.name)
            method()
        except:
            result.testFailed()
        self.tearDown()
        return result


class TestSuite:
    tests: list[TestCase]

    def __init__(self) -> None:
        self.tests = []
        
    def add(self, test: TestCase) -> None:
        self.tests.append(test)

    def run(self, result_collector: TestResult) -> None:
        results: list[TestResult] = [test.run() for test in self.tests]
        for test in self.tests:
            result = test.run()
            result_collector.runCount += result.runCount
            result_collector.failedCount += result.failedCount
        
        

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
