class TestStatus:
    name: str
    result: str
    info: str

    def __init__(self, name: str, result: str, info: str) -> None:
        self.name = name
        self.result = result
        self.info = info
