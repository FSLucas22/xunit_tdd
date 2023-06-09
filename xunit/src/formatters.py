from typing import Callable, Mapping
from .status import Status, TestStatus
import xunit.src.testcolours as color


formatter = Callable[[str], str]
test_status_formatter = Callable[[TestStatus], str]


basic_msg_formatter: test_status_formatter = lambda status: f'{status.name} - {status.result}'
error_msg_formatter: test_status_formatter = lambda status: f'{status.name} - {status.result}\n{status.info}'
detailed_msg_formatter: test_status_formatter = lambda status: f'{status.name} - {status.result}: {status.info}'


class TestStatusFormatter:
    def __init__(self, formatters: Mapping[Status, test_status_formatter]) -> None:
        self.formatters = formatters

    def __call__(self, test_status: TestStatus) -> str:
        formatter = self.formatters.get(test_status.result, detailed_msg_formatter)
        return formatter(test_status)


BASIC_FORMATTERS = TestStatusFormatter({
    Status.PASSED: lambda msg: color.green(basic_msg_formatter(msg)),
    Status.FAILED: lambda msg: color.red(basic_msg_formatter(msg)),
    Status.NOT_COMPLETED: lambda msg: color.yellow(basic_msg_formatter(msg)),
    Status.CREATED: lambda msg: color.blue(basic_msg_formatter(msg)),
    Status.FAILED_TO_RUN: lambda msg: color.yellow(basic_msg_formatter(msg))
})

BASIC_UNCOLORED_FORMATTERS = TestStatusFormatter({
    Status.PASSED: basic_msg_formatter,
    Status.FAILED: basic_msg_formatter,
    Status.NOT_COMPLETED: basic_msg_formatter
})

UNCOLORED_FORMATTERS = TestStatusFormatter({
    Status.PASSED: basic_msg_formatter,
    Status.FAILED: error_msg_formatter,
    Status.NOT_COMPLETED: error_msg_formatter,
    Status.FAILED_TO_RUN: error_msg_formatter
})

FORMATTERS = TestStatusFormatter({
    Status.PASSED: lambda msg: color.green(basic_msg_formatter(msg)),
    Status.FAILED: lambda msg: color.red(error_msg_formatter(msg)),
    Status.NOT_COMPLETED: lambda msg: color.yellow(error_msg_formatter(msg)),
    Status.CREATED: lambda msg: color.blue(detailed_msg_formatter(msg)),
    Status.FAILED_TO_RUN: lambda msg: color.yellow(error_msg_formatter(msg))
})
