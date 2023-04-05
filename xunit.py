class WasRun:
    wasRun: int | None
    def __init__(self, name: str):
        self.wasRun = None

    def testMethod(self) -> None:
        self.wasRun = 1

    def run(self) -> None:
        self.testMethod()


def main() -> None:
    test = WasRun("testMethod")
    print(test.wasRun)
    test.run()
    print(test.wasRun)


if __name__ == "__main__":
    main()
