from xunit.src import *
from typing import Type, NewType

@TestClass
class TestTest(TestCase):
    test_cls: Type[TestCase]
    
    def setUp(self) -> None:
        class UnnamedTestClass(TestCase):
            def testMethod(self) -> None:
                pass
        self.test_cls = UnnamedTestClass
        
    @Test
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

    @Test
    def testDecoratorReturnsSubClass(self) -> None:
        cls = Test(getattr(self.test_cls, "testMethod"))
        assert issubclass(cls, TestMethod)

    @Test    
    def testDecoratorInClassDontChangeTest(self) -> None:
        result_before_decorator = TestResult()
        result_after_decorator = TestResult()
        self.test_cls("testMethod").run(result_before_decorator)
        TestClass(self.test_cls)("testMethod").run(result_after_decorator)
        assert result_before_decorator.getAllPassed() ==\
               result_after_decorator.getAllPassed()

    @Test
    def testCanFindTestMethods(self) -> None:
        class SomeTestClass(TestCase):

            @Test
            def testMethod(self) -> None:
                pass

            @Test
            def anotherTestMethod(self) -> None:
                pass

            class notATestMethod:
                pass
        
        assert getTestMethods(SomeTestClass) == "testMethod anotherTestMethod"

    @Test
    def testNameIsAddedByDecorator(self) -> None:
        @TestClass
        class SomeTestClass(TestCase):
            testNames = "anotherTestMethod"
            @Test
            def testMethod(self) -> None:
                pass

            def anotherTestMethod(self) -> None:
                pass

        assert SomeTestClass.testNames == "anotherTestMethod testMethod"
