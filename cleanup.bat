@echo off
echo Killing all Python processes (Backend)...
taskkill /IM python.exe /F
echo.
echo Killing all Node.js processes (Frontend)...
taskkill /IM node.exe /F
echo.
echo Cleanup complete. You can now restart your servers.
pause
