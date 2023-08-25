@echo off
title "Run Check Apps Beta avaiable on Testflight"

CD /D %~dp0
set "Result_ErrorLinkTestflight=Result_ErrorLinkTestflight.txt"
set "Search_Text=testflight"

set "Result_BetaAppsAvailable=Result_BetaAppsAvailable.md"
set "Testflight_List=Testflight_List.txt"
set "Testflight_CheckStatus=Testflight_CheckStatus.py"
set "RemoveWebsiteError=RemoveWebsiteError.py"
set "README=README.md"

echo Running Python script...
python "%Testflight_CheckStatus%"
echo:

findstr %Search_Text% "%Result_ErrorLinkTestflight%" > nul

git pull origin master
if %errorlevel% equ 0 (
    echo Committing changes to Github...
	git add "%Result_BetaAppsAvailable%" "%README%"
    
    echo Remove Website Error...
	python "%RemoveWebsiteError%"
    git add "%Testflight_List%"
    git commit -m "Updated list beta apps"
    git push origin master
) else (
    echo Committing changes to Github...
	git add "%Result_BetaAppsAvailable%" "%README%"
)
git commit -m "Updated!"
git push origin master

exit /B