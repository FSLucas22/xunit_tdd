from xunit.src import *
from typing import Type, NewType


class TestTest(TestCase):
    testNames = "testDecoratorDontChangeTest testDecoratorInClassDontChangeTest"
    test_cls: Type[TestCase]
    
    def setUp(self) -> None:
        class UnnamedTestClass(TestCase):
            def testMethod(self) -> None:
                pass
        self.test_cls = UnnamedTestClass
        

    def testDecoratorDontChangeTest(self) -> None:
        result_before_decorator = TestResult()
        result_after_decorator = TestResult()
        self.test_cls("testMethod").run(result_before_decorator)
        setattr(self.test_cls, "testMethod", Test(
            getattr(self.test_cls, "testMethod")
        ))
        self.test_cls("testMethod").run(result_after_decorator)
        assert result_before_decorator.getAllPassed() ==\
               result_after_decorator.getAllPassed()


    def testDecoratorReturnsInstance(self) -> None:
        Test(getattr(self.test_cls, "testMethod"))
        assert type(getattr(self.test_cls, "testMethod")) == TestMethod
        
    def testDecoratorInClassDontChangeTest(self) -> None:
        result_before_decorator = TestResult()
        result_after_decorator = TestResult()
        self.test_cls("testMethod").run(result_before_decorator)
        TestClass(self.test_cls)("testMethod").run(result_after_decorator)
        assert result_before_decorator.getAllPassed() ==\
               result_after_decorator.getAllPassed()

    def testNameIsAddedByDecorator(self) -> None:
        class SomeTestClass(TestCase):

            @Test
            def testMethod(self) -> None:
                pass

        assert SomeTestClass.testNames == "testMethod"
