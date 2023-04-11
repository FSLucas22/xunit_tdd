from xunit.src import *
from xunit.tests.testclasses import UnnamedTestClass


class TestTest(TestCase):
    testNames = "testNameIsAddedByDecorator"
    
    def testNameIsAddedByDecorator(self) -> None:
        assert not hasattr(UnnamedTestClass, "testNames")
        setattr(UnnamedTestClass, "testMethod", Test(
            UnnamedTestClass, UnnamedTestClass.testMethod 
        ))
        assert UnnamedTestClass.testNames == "testMethod"
