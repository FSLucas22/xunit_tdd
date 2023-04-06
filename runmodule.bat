@echo off
mypy xunit tests.py --strict
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%
ECHO running module...
ECHO.
py tests.py
ECHO running module... done
EXIT /B %ERRORLEVEL%