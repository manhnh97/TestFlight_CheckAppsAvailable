@echo off
title "Run Check Apps Beta avaiable on Testflight"

CD /D %~dp0
set "Result_ErrorLinkTestflight=Result_ErrorLinkTestflight.txt"
set "stringTestflight=Testflight"

set "Result_BetaAppsAvailable=Result_BetaAppsAvailable.md"
set "Testflight_CheckStatus=Testflight_CheckStatus.py"
set "README=README.md"

echo Running Python script...
python "%Testflight_CheckStatus%"
echo:

set "found="
for /f "usebackq delims=" %%a in ("%Result_ErrorLinkTestflight%") do (
    echo %%a | findstr /C:"%stringTestflight%" >nul && set "found=1"
)

if defined found (
    echo Committing changes to Github...
	git add "%Result_BetaAppsAvailable%" "%Testflight_CheckStatus%" "%README%"
	git commit -m "Updated!"
	git push origin master
) else (
    echo Committing changes to Github...
	git add "%Result_BetaAppsAvailable%" "%README%"
	git commit -m "Updated!"
	git push origin master
)
exit /B