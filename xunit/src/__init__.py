from xunit.src.testcase import *
from xunit.src.testresult import *
from xunit.src.testsummary import *
from xunit.src.testsuite import *
from xunit.src.testdecorator import *
from xunit.src.testexceptions import *
from xunit.src.testerrorinfo import *
from xunit.src.testcolors import *
from xunit.src.packagemanager import *
from typing import Type, Callable
from types import ModuleType


def run(
    subject: Type[TestCase] | ModuleType | str,
    type: str,
    capture_output: Callable[[str], None]
    ) -> None:
    pass
