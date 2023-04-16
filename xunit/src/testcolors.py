from termcolor import colored


def green(text: str) -> str:
    return colored(text, 'green')


def red(text: str) -> str:
    return colored(text, 'red')


def yellow(text: str) -> str:
    return colored(text, 'yellow')
