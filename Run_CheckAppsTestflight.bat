@echo off
setlocal enabledelayedexpansion
title Check Apps Beta available on Testflight
CD /D %~dp0

:gitPull
git pull origin master
if %errorlevel% neq 0 (
    echo Restoring code to the previous state...
    git restore --source=HEAD --staged --worktree -- "Result_BetaAppsAvailable.md" "Testflight_List.txt"
    exit /B
)
goto :eof

:pythonScript
set "Testflight_CheckStatus=main.py"
echo Run "%Testflight_CheckStatus%" script...
python "%Testflight_CheckStatus%"
if %errorlevel% neq 0 (
    echo Restoring code to the previous state...
    git restore --source=HEAD --staged --worktree -- "Result_BetaAppsAvailable.md" "Testflight_List.txt"
    exit /B
)
goto :eof

:commitGITHUB
git add "Result_BetaAppsAvailable.md" "Testflight_List.txt"
git commit -m "Updated!"
git push origin master

rundll32 user32.dll,MessageBeep
exit /B
