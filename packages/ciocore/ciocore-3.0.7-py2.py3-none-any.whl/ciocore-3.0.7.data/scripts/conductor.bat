@echo off

REM Search the PATH for all Pythons and if we find Python3 then use it.
REM If we don't find Python3, then use the first Python.
REM If that fails, ask the user to install Python 

FOR /f %%p in ('where python') do (
    echo %%p | findstr /C:"Python3">nul && (
        echo Found Python at: %%p
        %%p "%~dp0\conductor" %*
        GOTO :EOF
    ) 
)
FOR /f %%p in ('where python') do (
    %%p "%~dp0\conductor" %*
    GOTO :EOF
)

echo WARNING: Can't find a python installation.
echo Please install Python, add it to your PATH and try again.

