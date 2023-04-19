from xunit.src import *
from typing import Type, NewType

@TestClass
class TestTest(TestCase):
    test_cls: Type[TestCase]
    
    def setup(self) -> None:
        class UnnamedTestClass(TestCase):
            def test_method(self) -> None:
                pass

            def broken_method(self) -> None:
                raise Exception
            
        self.test_cls = UnnamedTestClass
    
    @Test    
    def test_decorator_dont_change_test(self) -> None:
        result_before_decorator = TestResult()
        result_after_decorator = TestResult()
        self.test_cls("test_method").run(result_before_decorator)
        self.test_cls("broken_method").run(result_before_decorator)
        setattr(self.test_cls, "test_method", Test(
            getattr(self.test_cls, "test_method")
        ))
        setattr(self.test_cls, "broken_method", Test(
            getattr(self.test_cls, "broken_method")
        ))
        self.test_cls("test_method").run(result_after_decorator)
        self.test_cls("broken_method").run(result_after_decorator)
        assert result_before_decorator.passed ==\
               result_after_decorator.passed
        assert result_before_decorator.failed ==\
               result_after_decorator.failed
        
    @Test
    def test_decorator_returns_flag(self) -> None:
        test_method = Test(getattr(self.test_cls, "test_method"))
        attr = getattr(test_method, "_is_test_method")
        assert attr
        
    @Test
    def test_is_equal_with_decorator_sintax(self) -> None:
        @TestClass
        class UnnamedTestClass(TestCase):
            @Test
            def test_method(self) -> None:
                pass

            @Test
            def broken_method(self) -> None:
                raise Exception

        suite = TestSuite.from_test_case(UnnamedTestClass)
        result = TestResult()
        suite.run(result)
        assert result.passed == "test_method"
        assert result.failed == "broken_method"

    @Test
    def test_is_equal_when_fails_in_set_up(self) -> None:
        @TestClass
        class BrokenUnnamedTestClass(TestCase):
            def setup(self) -> None:
                raise Exception
            
            @Test
            def test_method(self) -> None:
                pass

            @Test
            def broken_method(self) -> None:
                raise Exception

        @TestClass
        class UnnamedTestClass(TestCase):
            
            @Test
            def test_method1(self) -> None:
                pass

            @Test
            def broken_method1(self) -> None:
                raise Exception

        suite = TestSuite.from_test_case(
            BrokenUnnamedTestClass, UnnamedTestClass)
        result = TestResult()
        suite.run(result)
        assert result.passed_count == 1
        assert result.failed_count == 1
        assert result.not_completed_count == 2
        

    @Test
    def test_attributes_added_by_decorator(self) -> None:
        @TestClass
        class SomeTestClass(TestCase):
            
            @Test
            def test_method(self) -> None:
                pass

            @Test
            def another_test_method(self) -> None:
                pass

        assert SomeTestClass.testNames == "test_method another_test_method"
        assert SomeTestClass._is_xunit_test_class == True

    @Test
    def test_cannot_have_names_when_decorated(self) -> None:
        try:
            @TestClass
            class SomeTestClass(TestCase):
                testNames = "another_test_method"
                
                @Test
                def test_method(self) -> None:
                    pass

                def another_test_method(self) -> None:
                    pass
      
        except InvalidAttributeException as e:
            return

        raise AssertionError
        
        
