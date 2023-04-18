import xunit
import xunittest


@xunit.TestClass
class TestXunit(xunit.TestCase):

    @xunit.Test
    def testXunitRunsSuiteFromCommandLine(self) -> None:
        suite = xunit.TestSuite.fromModule(xunittest)
        result = xunit.TestResult()
        suite.run(result)
        assert result.getAllPassed() == "testMethod testMethod2"
        assert result.getAllFailed() == "failedMethod"
        
