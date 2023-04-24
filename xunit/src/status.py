class TestStatus:

    def __init__(self, name: str, result: str, info: str) -> None:
        self._name = name
        self._result = result
        self._info = info

    @property
    def name(self) -> str:
        return self._name

    @property
    def result(self) -> str:
        return self._result

    @property
    def info(self) -> str:
        return self._info
