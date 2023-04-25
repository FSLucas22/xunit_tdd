from typing import Callable
from xunit.src.status import TestStatus


Observer = Callable[[TestStatus], None]
