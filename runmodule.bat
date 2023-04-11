@echo off
mypy xunit --strict
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%
ECHO running module...
ECHO.
py -m xunit
ECHO running module... done
EXIT /B %ERRORLEVEL%