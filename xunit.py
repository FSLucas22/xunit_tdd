class TestCase:
    name: str
    
    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def run(self) -> None:
        self.setUp()
        method = getattr(self, self.name)
        method()
        

class WasRun(TestCase):
    wasRun: int | None
    wasSetUp: int | None

    def setUp(self) -> None:
        self.wasRun = None
        self.wasSetUp = 1

    def testMethod(self) -> None:
       self.wasRun = 1


class TestCaseTest(TestCase):
    test: WasRun
    
    def setUp(self) -> None:
        self.test = WasRun("testMethod")
    
    def testRunning(self) -> None:
        self.test.run()
        assert self.test.wasRun == 1

    def testSetUp(self) -> None:
        self.test.run()
        assert self.test.wasSetUp == 1


def main() -> None:
    TestCaseTest("testRunning").run()
    TestCaseTest("testSetUp").run()


if __name__ == "__main__":
    main()
