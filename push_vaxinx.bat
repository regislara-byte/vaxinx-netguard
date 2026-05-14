@echo off
title VAXINX Netguard Git Push

echo.
echo ================================
echo      VAXINX QUICK PUSH
echo ================================
echo.

git add .

set /p msg=Enter commit message: 
git commit -m "%msg%"

git push

echo.
echo Opening live site...
timeout /t 2 >nul

start "" "https://regislara-byte.github.io/vaxinx-netguard/dashboard/"

echo.
echo ================================
echo DEPLOY COMPLETE
echo ================================
pause