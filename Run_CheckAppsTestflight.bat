@echo off
setlocal enabledelayedexpansion
title Check Apps Beta available on Testflight
CD /D %~dp0

git pull origin master    

python "main.py"

timeout 3
git add "Testflight_List.txt" "Result_Available_BetaApps.md" "Result_Full_BetaApps.md"
git commit -m "Updated!"
git push origin master

exit /B
