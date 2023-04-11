class Log:
    executed: str

    def __init__(self) -> None:
        self.executed = ""
        
    def register(self, name: str) -> None:
        if self.executed != "":
            self.executed += " "
        self.executed += name

    def registerCount(self) -> int:
        return len(self.executed.split())


class TestResult:
    failed: Log
    passed: Log
    notCompleted: Log
    
    def __init__(self) -> None:
        self.failed = Log()
        self.notCompleted = Log()
        self.passed = Log()
        
    def testNotCompleted(self, test_name: str) -> None:
        self.notCompleted.register(test_name)

    def testPassed(self, test_name: str) -> None:
        self.passed.register(test_name)

    def testFailed(self, test_name: str) -> None:
        self.failed.register(test_name)

    @property
    def runCount(self) -> int:
        return self.passed.registerCount() + self.failed.registerCount() 

    @property
    def failedCount(self) -> int:
        return self.failed.registerCount()

    @property
    def notCompletedCount(self) -> int:
        return self.notCompleted.registerCount()

    @property
    def passedCount(self) -> int:
        return self.passed.registerCount()

    def getAllStarted(self) -> str:
        started = Log()
        for passed in self.getAllPassed().split():
            started.register(passed)
        for failed in self.getAllFailed().split():
            started.register(failed)
        return started.executed

    def getAllFailed(self) -> str:
        return self.failed.executed

    def getAllPassed(self) -> str:
        return self.passed.executed

    def getAllNotCompleted(self) -> str:
        return self.notCompleted.executed


class TestSummary:
    def results(self, result: TestResult) -> str:
        return f"{result.runCount} run, {result.failedCount} failed, {result.notCompletedCount} not completed"


class DetailedTestSummary:
    def results(self, result: TestResult) -> str:
        summary = ""
        for test in result.getAllFailed().split():
            summary += test + ' - Failed\n'
        for test in result.getAllPassed().split():
            summary += test + ' - Passed\n'
        for test in result.getAllNotCompleted().split():
            summary += test + ' - Not completed\n'
        return summary[:-1]


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
