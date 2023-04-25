from typing import Callable, Protocol
from xunit.src.status import TestStatus


Observer = Callable[[TestStatus], None]


class Subject(Protocol):
    def register(self, observer: Observer) -> None:
        ...

    def notify(self, status: TestStatus) -> None:
        ...
