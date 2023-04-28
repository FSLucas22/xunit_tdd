from xunit.src import *
from xunit.src.status import TestStatus, Status
from xunit.src.observer import *
from xunit.tests.testclasses import DummyObserver
from typing import cast


@TestClass
class TestSubject(TestCase):

    @Test
    def test_observer(self) -> None:
        observer: Observer = DummyObserver()
        status = TestStatus("x", Status.PASSED, "z")
        observer(status)
        observer = cast(DummyObserver, observer)
        assert observer.received == [status]
        observer(status)
        assert observer.received == [status, status]
    
    @Test
    def test_subject(self) -> None:
        observer1 = DummyObserver()
        observer2 = DummyObserver()
        subject: Subject = SubjectImp(observer1, observer2) 
        status = TestStatus("x", Status.PASSED, "z")
        
        subject.notify(status)
        
        assert observer1.received == observer2.received == [status]
        
        subject.unregister(observer1)
        
        subject.notify(status)
        
        assert observer1.received == [status]
        assert observer2.received == [status, status]
