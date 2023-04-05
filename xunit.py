class TestCase:
    name: str
    
    def __init__(self, name: str):
        self.name = name

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def run(self) -> None:
        self.setUp()
        method = getattr(self, self.name)
        method()
        self.tearDown()
        

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


class TestCaseTest(TestCase):
    test: WasRun

    def testTemplateMethod(self) -> None:
        self.test = WasRun("testMethod")
        self.test.run()
        assert self.test.log == "setUp testMethod tearDown"

    def testResult(self) -> None:
        test = WasRun("testMethod")
        result = test.run() # type: ignore
        assert "1 run, 0 failed" == result.summary()


def main() -> None:
    TestCaseTest("testTemplateMethod").run()
    TestCaseTest("testResult").run()


if __name__ == "__main__":
    main()
