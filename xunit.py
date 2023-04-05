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


def main() -> None:
    test = WasRun("testMethod")
    print(test.wasRun)
    test.run()
    print(test.wasRun)


if __name__ == "__main__":
    main()
