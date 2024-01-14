@echo off
setlocal enabledelayedexpansion
title Check Apps Beta available on Testflight
CD /D %~dp0

:: Trap Ctrl+C
set "trap=false"
set "trap_cmd=goto :handleCtrlC"

:: Define Ctrl+C handler
:handleCtrlC
echo.
echo Ctrl+C detected. Restoring code to the previous state...
git restore "Result_BetaAppsAvailable.md" "Testflight_List.txt"
echo Exiting...
exit /B

:: Register Ctrl+C handler
if not "%trap%"=="false" goto :registerCtrlCHandler
set "trap=true"
echo( & echo( & set "trap=false" & call "%0" %* & exit /B %errorlevel%

:registerCtrlCHandler
call :CtrlCHandler
if "%errorlevel%"=="0" exit /B 0
goto :exit

:CtrlCHandler
for /f %%a in ('copy /Z "%~dpf0" nul') do set "CTRL_Z=%%a"
if not defined OS goto :checkOS
if /i "%OS%"=="Windows_NT" goto :checkOS

:checkOS
if exist "%SystemRoot%\system32\find.exe" set "FIND=%SystemRoot%\system32\find.exe" & goto :eof
if exist "%SystemRoot%\system\find.exe" set "FIND=%SystemRoot%\system\find.exe" & goto :eof
echo Error: FIND.EXE not found.
exit /B 1

:gitPull
git pull origin master
if %errorlevel% neq 0 (
    echo Restoring code to the previous state...
    git restore "Result_BetaAppsAvailable.md" "Testflight_List.txt"
    exit /B
)
goto :eof

:pythonScript
set "Testflight_CheckStatus=main.py"
echo Run "%Testflight_CheckStatus%" script...
python "%Testflight_CheckStatus%"
if %errorlevel% neq 0 (
    echo Restoring code to the previous state...
    git restore "Result_BetaAppsAvailable.md" "Testflight_List.txt"
    exit /B
)
goto :eof

:commitGITHUB
git add "Result_BetaAppsAvailable.md" "Testflight_List.txt"
git commit -m "Updated!"
git push origin master

rundll32 user32.dll,MessageBeep
goto :exit

:exit
exit /B
