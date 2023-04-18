import xunit


@xunit.TestClass
class Test(xunit.TestCase):

    @xunit.Test
    def testMethod(self) -> None:
        pass

    @xunit.Test
    def failedMethod(self) -> None:
        raise Exception
