from xunit.src import *
from typing import Type, NewType

@TestClass
class TestTest(TestCase):
    test_cls: Type[TestCase]
    
    def setUp(self) -> None:
        class UnnamedTestClass(TestCase):
            def testMethod(self) -> None:
                pass

            def brokenMethod(self) -> None:
                raise Exception
            
        self.test_cls = UnnamedTestClass
    
    @Test    
    def testDecoratorDontChangeTest(self) -> None:
        result_before_decorator = TestResult()
        result_after_decorator = TestResult()
        self.test_cls("testMethod").run(result_before_decorator)
        self.test_cls("brokenMethod").run(result_before_decorator)
        setattr(self.test_cls, "testMethod", Test(
            getattr(self.test_cls, "testMethod")
        ))
        setattr(self.test_cls, "brokenMethod", Test(
            getattr(self.test_cls, "brokenMethod")
        ))
        self.test_cls("testMethod").run(result_after_decorator)
        self.test_cls("brokenMethod").run(result_after_decorator)
        assert result_before_decorator.getAllPassed() ==\
               result_after_decorator.getAllPassed()
        assert result_before_decorator.getAllFailed() ==\
               result_after_decorator.getAllFailed()
        
    @Test
    def testDecoratorReturnsFlag(self) -> None:
        test_method = Test(getattr(self.test_cls, "testMethod"))
        attr = getattr(test_method, "_is_test_method")
        assert attr
   
    def testDecoratorInClassDontChangeTest(self) -> None:
        result_before_decorator = TestResult()
        result_after_decorator = TestResult()
        self.test_cls("testMethod").run(result_before_decorator)
        TestClass(self.test_cls)("testMethod").run(result_after_decorator)
        self.test_cls("brokenMethod").run(result_before_decorator)
        TestClass(self.test_cls)("brokenMethod").run(result_after_decorator)
        
        assert result_before_decorator.getAllPassed() ==\
               result_after_decorator.getAllPassed()
        assert result_before_decorator.getAllFailed() ==\
               result_after_decorator.getAllFailed()

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
    def testIsEqualWithNewSintax(self) -> None:
        @TestClass
        class UnnamedTestClass(TestCase):
            @Test
            def testMethod(self) -> None:
                pass

            @Test
            def brokenMethod(self) -> None:
                raise Exception

        suite = TestSuite.fromTestCase(UnnamedTestClass)
        result = TestResult()
        suite.run(result)
        assert result.getAllPassed() == "testMethod"
        assert result.getAllFailed() == "brokenMethod"

    @Test
    def testIsEqualWhenFailsInSetUp(self) -> None:
        @TestClass
        class BrokenUnnamedTestClass(TestCase):
            def setUp(self) -> None:
                raise Exception
            
            @Test
            def testMethod(self) -> None:
                pass

            @Test
            def brokenMethod(self) -> None:
                raise Exception

        @TestClass
        class UnnamedTestClass(TestCase):
            
            @Test
            def testMethod1(self) -> None:
                pass

            @Test
            def brokenMethod1(self) -> None:
                raise Exception

        suite = TestSuite.fromTestCase(BrokenUnnamedTestClass, UnnamedTestClass)
        result = TestResult()
        suite.run(result)
        assert result.passedCount == 1
        assert result.failedCount == 1
        assert result.notCompletedCount == 2
        

    @Test
    def testAttributesAddedByDecorator(self) -> None:
        @TestClass
        class SomeTestClass(TestCase):
            
            @Test
            def testMethod(self) -> None:
                pass

            @Test
            def anotherTestMethod(self) -> None:
                pass

        assert SomeTestClass.testNames == "testMethod anotherTestMethod"
        assert SomeTestClass._is_xunit_test_class == True

    @Test
    def testCannotHaveNamesWhenDecorated(self) -> None:
        try:
            @TestClass
            class SomeTestClass(TestCase):
                testNames = "anotherTestMethod"
                
                @Test
                def testMethod(self) -> None:
                    pass

                def anotherTestMethod(self) -> None:
                    pass
      
        except InvalidAttributeException as e:
            return

        raise AssertionError
        
        
