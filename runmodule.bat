@echo off
mypy xunit.py --strict
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%
ECHO running module...
ECHO.
py xunit.py
ECHO running module... done
EXIT /B %ERRORLEVEL%