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
        test1 = self.test_cls("test_method")
        test2 = self.test_cls("broken_method")
        test1.register(result_before_decorator.save_status)
        test2.register(result_before_decorator.save_status)
        test1.run()
        test2.run()
        
        setattr(self.test_cls, "test_method", Test(
            getattr(self.test_cls, "test_method")
        ))
        setattr(self.test_cls, "broken_method", Test(
            getattr(self.test_cls, "broken_method")
        ))
        
        test1 = self.test_cls("test_method")
        test2 = self.test_cls("broken_method")
        test1.register(result_after_decorator.save_status)
        test2.register(result_after_decorator.save_status)
        test1.run()
        test2.run()
        
        assert result_before_decorator.get_names_of_status(Status.PASSED) ==\
               result_after_decorator.get_names_of_status(Status.PASSED)
        assert result_before_decorator.get_names_of_status(Status.FAILED) ==\
               result_after_decorator.get_names_of_status(Status.FAILED)
        
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

        suite = SuiteFactoryImp().from_test_case(UnnamedTestClass)
        result = TestResult()
        suite.register(result.save_status)
        suite.run()
        assert result.get_names_of_status(Status.PASSED) == "test_method"
        assert result.get_names_of_status(Status.FAILED) == "broken_method"

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

        suite = SuiteFactoryImp().from_test_case(
            BrokenUnnamedTestClass, UnnamedTestClass)
        result = TestResult()
        suite.register(result.save_status)
        suite.run()
        assert result.get_status_count(Status.PASSED) == 1
        assert result.get_status_count(Status.FAILED) == 1
        assert result.get_status_count(Status.NOT_COMPLETED) == 2
        

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

        assert SomeTestClass.xunit_test_names == "test_method another_test_method"
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
        
        
