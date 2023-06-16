from src.xunit import *
from src.xunit.status import TestStatus, Status
from src.xunit.observer import *
from .testclasses import DummyObserver
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
    def test_unregister(self) -> None:
        observer1 = DummyObserver()
        observer2 = DummyObserver()
        subject: Subject = SubjectImp(observer1, observer2) 
        status = TestStatus("x", Status.PASSED, "z")
        
        subject.unregister(observer1, observer2)
        
        subject.notify(status)
        
        assert observer1.received == []
        assert observer2.received == []
    
    @Test
    def test_only_unregister_correct_observer(self) -> None:
        observer1 = DummyObserver()
        observer2 = DummyObserver()
        observer3 = DummyObserver()
        subject: Subject = SubjectImp(observer1, observer2, observer3) 
        status = TestStatus("x", Status.PASSED, "z")
        
        subject.unregister(observer2)
        subject.notify(status)
        
        assert observer1.received == [status] == observer3.received
        assert observer2.received == []
        
    
    @Test
    def test_register(self) -> None:
        observer1 = DummyObserver()
        observer2 = DummyObserver()
        subject: Subject = SubjectImp(observer1)
        subject.register(observer2)
        status = TestStatus("x", Status.PASSED, "z")
        subject.notify(status)
        
        assert observer1.received == observer2.received == [status]
