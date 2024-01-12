@echo off
setlocal enabledelayedexpansion
title Check Apps Beta avaiable on Testflight
CD /D %~dp0

git pull origin master
if %errorlevel% neq 0 (
    echo Restoring code to the previous state...
    git restore "Result_BetaAppsAvailable.md" "Testflight_List.txt"
	
	goto :exit
)
set "Testflight_CheckStatus=main.py"
echo Run "%Testflight_CheckStatus%" script...
python "%Testflight_CheckStatus%"

echo:

goto :commitGITHUB

:commitGITHUB
    git add "Result_BetaAppsAvailable.md" "Testflight_List.txt"
    git commit -m "Updated!"
    git push origin master

    rundll32 user32.dll,MessageBeep
goto :exit

:exit
    exit /B
