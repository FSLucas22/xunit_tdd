from typing import Callable, Protocol
from xunit.src.status import TestStatus


Observer = Callable[[TestStatus], None]


class Subject(Protocol):
    def register(self, *observer: Observer) -> None:
        ...

    def notify(self, status: TestStatus) -> None:
        ...

    def unregister(self, *observer: Observer) -> None:
        ...


class SubjectImp:
    def __init__(self, *observers: Observer) -> None:
        self._observers = list(observers)

    def register(self, *observers: Observer) -> None:
        self._observers += list(observers)

    def unregister(self, *observers: Observer) -> None:
        for observer in self._observers:
            if observer in self._observers:
                self._observers.remove(observer)

    def notify(self, status: TestStatus) -> None:
        for observer in self._observers:
            observer(status)
