import xunit
import xunittest
import colorama
import os


@xunit.TestClass
class TestXunit(xunit.TestCase):

    @xunit.Test
    def testXunitRunsSuiteFromCommandLine(self) -> None:
        suite = xunit.TestSuite.fromModule(xunittest)
        result = xunit.TestResult()
        suite.run(result)
        assert result.getAllPassed() == "testMethod"
        assert result.getAllFailed() == "failedMethod"


def main() -> None:
    
    result = xunit.TestResult()
    summary = xunit.MixedTestSummary(
        xunit.PassedSummary(passed_formatter=xunit.green),
        xunit.ErrorInfoSummary(
            failed_formatter=xunit.red, notCompleted_formatter=xunit.yellow),
        xunit.SimpleTestSummary()
    )
    suite = xunit.TestSuite.fromTestCase(TestXunit)
    suite.run(result)
    print(summary.results(result))

if __name__ == "__main__":
    if os.name == "nt":
        colorama.init()
    main()
    if os.name == "nt":
        colorama.deinit()
