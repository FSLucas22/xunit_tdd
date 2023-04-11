from xunit.src import *
from xunit.tests.testclasses import UnnamedTestClass


class TestTest(TestCase):
    testNames = "testNameIsAddedByDecorator"
    
    def testNameIsAddedByDecorator(self) -> None:
        assert not hasattr(UnnamedTestClass, "testNames")
        Test(UnnamedTestClass.testMethod, UnnamedTestClass)
        assert UnnamedTestClass.testNames == "testMethod"
