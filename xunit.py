class TestCase:
    name: str
    def __init__(self, name: str):
        self.name = name

    def run(self) -> None:
        method = getattr(self, self.name)
        method()
        

class WasRun(TestCase):
    wasRun: int | None
    
    def __init__(self, name: str):
        self.wasRun = None
        super().__init__(name)

    def testMethod(self) -> None:
       self.wasRun = 1


class TestCaseTest(TestCase):
    def testRunning(self) -> None:
        test = WasRun("testMethod")
        assert test.wasRun is None
        test.run()
        assert test.wasRun == 1


def main() -> None:
    TestCaseTest("testRunning").run()


if __name__ == "__main__":
    main()
