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
