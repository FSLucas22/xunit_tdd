from xunit.src import *
from xunit.src import loader
from xunit.tests.testclasses import *


@TestClass
class SuiteFactoryTest(TestCase):
    result: TestResult
    suite: TestSuite

    def setup(self) -> None:
        self.result = TestResult()
        self.suite = TestSuite(self.result.save_status)

    @Test
    def test_tests_from_class(self) -> None:
        self.suite.add(*loader.tests_from_class(PassedTestCase, FailedTestCase))
        self.suite.run()
  
        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "passed_test failed_test"

    @Test
    def test_tests_from_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        self.suite.add(*loader.tests_from_module(testmodule))
        self.suite.run()

        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "someTest someOtherTest"

    @Test
    def test_tests_from_package(self) -> None:
        import xunit.tests.testpackage as testpackage
        self.suite.add(*loader.tests_from_package(testpackage, lambda _, __: False))
        self.suite.run()

        passed = self.result.get_names_of_status(Status.PASSED)
        failed = self.result.get_names_of_status(Status.FAILED)

        assert "x" in passed and "y" in passed and "z" in passed
        assert "x1" in failed and "y1" in failed and "z1" in failed

    @Test
    def test_ignore(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackage"]
        self.suite.add(*loader.tests_from_package(testpackage, ignore=ignore))
        self.suite.run()
        assert "y y1" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)

    @Test
    def test_ignore_perpetuates(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackagemodule"]
        self.suite.add(*loader.tests_from_package(testpackage, ignore=ignore))
        self.suite.run()
        assert "y y1" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)
