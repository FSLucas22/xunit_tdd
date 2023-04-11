from xunit.src.log import Log


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