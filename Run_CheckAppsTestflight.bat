@echo off
setlocal enabledelayedexpansion
title Check Apps Beta avaiable on Testflight
CD /D %~dp0

git pull origin master
set "Testflight_CheckStatus=Testflight_CheckStatus.py"
echo Run "%Testflight_CheckStatus%" script...
python "%Testflight_CheckStatus%"
if %errorlevel% neq 0 (
    goto :exit
)
echo:
set "Result_ErrorLinkTestflight=Result_ErrorLinkTestflight.txt"
echo Check if the file "%Result_ErrorLinkTestflight%" exists...
if not exist "%Result_ErrorLinkTestflight%" (
    goto :exit
)
echo:
echo Check if the file "%Result_ErrorLinkTestflight%" contains the string "testflight"
set "Result_BetaAppsAvailable=Result_BetaAppsAvailable.md"
set "Testflight_List=Testflight_List.txt"
set "RemoveWebsiteError=RemoveWebsiteError.py"
set "README=README.md"
set "found=false"
for /f "usebackq delims=" %%a in ("file.txt") do (
    if "%%a"=="testflight" (
        set "found=true"
        goto :found
    )
)

:notfound
	echo Committing changes to Github...
	git add "%Result_BetaAppsAvailable%" 
goto :commitGITHUB

:found
	echo Committing changes to Github...
	git add "%Result_BetaAppsAvailable%" 

	echo Remove Website Error...
	python "%RemoveWebsiteError%"
	git add "%Testflight_List%"
	git commit -m "Updated list beta apps"
	git push origin master
goto :commitGITHUB

:commitGITHUB
	git commit -m "Updated!"
	git push origin master
goto :exit
	
:exit
	exit /B