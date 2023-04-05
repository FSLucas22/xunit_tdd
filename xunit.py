class WasRun:
    wasRun: int | None
    def __init__(self, name: str):
        self.wasRun = None

    def testMethod(self) -> None:
        self.wasRun = 1


def main() -> None:
    test = WasRun("testMethod")
    print(test.wasRun)
    test.testMethod()
    print(test.wasRun)


if __name__ == "__main__":
    main()
