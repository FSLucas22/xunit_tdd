from xunit.src.status import *
from xunit.src.observer import Observer, SubjectImp


class TestCase(SubjectImp):
    name: str
    xunit_test_names: str
    _is_xunit_test_class: bool
    
    def __init__(self, name: str, *observers: Observer):
        self.name = name
        super().__init__(*observers)

    def setup(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def run(self) -> None:
        try:
            self.setup()
            method = getattr(self, self.name)
        except Exception as e:
            info = TestStatus.from_exception(e, self.name, Status.NOT_COMPLETED)
            self.notify(info)
            self.teardown()
            return
        try:
            method()
            info = TestStatus(self.name, Status.PASSED, "-")
        except Exception as e:
            info = TestStatus.from_exception(e, self.name, Status.FAILED)
        self.notify(info)
        self.teardown()
