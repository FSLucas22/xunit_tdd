class WasRun:
    wasRun: int | None
    name: str
    
    def __init__(self, name: str):
        self.wasRun = None
        self.name = name

    def testMethod(self) -> None:
       self.wasRun = 1

    def run(self) -> None:
        method = getattr(self, self.name)
        method()


def main() -> None:
    test = WasRun("testMethod")
    print(test.wasRun)
    test.run()
    print(test.wasRun)


if __name__ == "__main__":
    main()
