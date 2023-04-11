from xunit.src import *
from xunit.tests.testclasses import UnnamedTestClass


class TestTest(TestCase):
    testNames = "testNameIsAddedByDecorator"
    
    def testNameIsAddedByDecorator(self) -> None:
        assert not hasattr(UnnamedTestClass, "testNames")
        result_before_decorator = TestResult()
        result_after_decorator = TestResult()
        UnnamedTestClass("testMethod").run(result_before_decorator)
        setattr(UnnamedTestClass, "testMethod", Test(
            UnnamedTestClass, UnnamedTestClass.testMethod 
        ))
        assert UnnamedTestClass.testNames == "testMethod"
        UnnamedTestClass("testMethod").run(result_after_decorator)
        assert result_before_decorator.getAllPassed() ==\
               result_after_decorator.getAllPassed()
