@echo off
title "Run Check Apps Beta avaiable on Testflight"

CD /D %~dp0

echo Running Python script...
python Testflight_CheckStatus.py
echo:
echo Committing changes to Github...
git add Result_BetaAppsAvailable.md README.md
git commit -m "Updated!"
git push origin master

exit /B