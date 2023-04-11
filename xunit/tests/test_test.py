from xunit.src import *
from xunit.tests.testclasses import UnnamedTestClass


class TestTest(TestCase):
    testNames = "testDecoratorDontChangeTest testDecoratorReturnsInstance"

    def testDecoratorDontChangeTest(self) -> None:
        result_before_decorator = TestResult()
        result_after_decorator = TestResult()
        UnnamedTestClass("testMethod").run(result_before_decorator)
        setattr(UnnamedTestClass, "testMethod", Test(
            UnnamedTestClass.testMethod
        ))
        UnnamedTestClass("testMethod").run(result_after_decorator)
        assert result_before_decorator.getAllPassed() ==\
               result_after_decorator.getAllPassed()

    def testDecoratorReturnsInstance(self) -> None:
        assert isinstance(
            Test(UnnamedTestClass.testMethod), TestClassMethod
        )

    def testNameIsAddedByDecorator(self) -> None:
        class SomeTestClass(TestCase):

            @Test
            def testMethod(self) -> None:
                pass

        assert SomeTestClass.testNames == "testMethod"
