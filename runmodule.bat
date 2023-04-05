@echo off
mypy xunit.py --strict
IF %ERRORLEVEL% NEQ 0 EXIT 1
ECHO running module...
ECHO.
py xunit.py