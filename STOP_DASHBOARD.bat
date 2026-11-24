@echo off
echo ========================================
echo   STOPPING DASHBOARD SERVERS
echo ========================================
echo.

echo Stopping Python processes...
taskkill /F /IM python.exe /T > nul 2>&1

echo.
echo ========================================
echo   ALL SERVERS STOPPED
echo ========================================
echo.
pause
