from xunit.src import *
from xunit.tests.testclasses import *


@TestClass
class SuiteFactoryTest(TestCase):
    result: TestResult
    factory: VerboseSuiteFactory

    def setup(self) -> None:
        self.result = TestResult()
        self.factory = VerboseSuiteFactory()

    @Test
    def test_suite_from_multiple_test_cases(self) -> None:
        self.factory.from_test_case(
            PassedTestCase, FailedTestCase,
            observers=[self.result.save_status]).run()
  
        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "passed_test failed_test"

    @Test
    def test_test_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = self.factory.from_test_case(
            testmodule.SomeTest,
            testmodule.SomeOtherTest,
            observers=[self.result.save_status]
        )
        suite.run()
        assert self.result.get_names_of_status(Status.PASSED, Status.FAILED) == "someTest someOtherTest"

    @Test
    def test_from_module(self) -> None:
        import xunit.tests.testmodule as testmodule
        suite = self.factory.from_module(testmodule, testmodule, observers=[self.result.save_status])
        suite.run()
        assert self.result.get_names_of_status(
            Status.PASSED, Status.FAILED) == "someTest someTest someOtherTest someOtherTest"

    @Test
    def test_from_package(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda _, __: False
        suite = self.factory.from_package(testpackage, ignore=ignore, observers=[self.result.save_status])
        suite.run()
        passed = self.result.get_names_of_status(Status.PASSED)
        failed = self.result.get_names_of_status(Status.FAILED)
        assert "x" in passed and "y" in passed and "z" in passed
        assert "x1" in failed and "y1" in failed and "z1" in failed

    @Test
    def test_ignore(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackage"]
        suite = self.factory.from_package(testpackage, ignore=ignore, observers=[self.result.save_status])
        suite.run()
        assert "y y1" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)

    @Test
    def test_ignore_perpetuates(self) -> None:
        import xunit.tests.testpackage as testpackage
        ignore = lambda obj, pkg: obj.name in ["packagemodule", "subpackagemodule"]
        suite = self.factory.from_package(testpackage, ignore=ignore, observers=[self.result.save_status])
        suite.run()
        assert "y y1" == self.result.get_names_of_status(Status.PASSED, Status.FAILED)
