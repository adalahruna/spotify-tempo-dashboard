@echo off
echo ========================================
echo   SPOTIFY DASHBOARD - AUTO START
echo ========================================
echo.

REM Start Flask API in new window
echo Starting Flask API...
start "Flask API - PORT 5000" cmd /k "cd /d %~dp0 && python api/search_api.py"

REM Wait 3 seconds for API to start
timeout /t 3 /nobreak > nul

REM Start Dashboard server in new window  
echo Starting Dashboard...
start "Dashboard - PORT 8000" cmd /k "cd /d %~dp0dashboard && python -m http.server 8000"

REM Wait 2 seconds for dashboard to start
timeout /t 2 /nobreak > nul

REM Open browser
echo Opening browser...
start http://localhost:8000/simple.html

echo.
echo ========================================
echo   DASHBOARD STARTED!
echo ========================================
echo.
echo Flask API:    http://localhost:5000
echo Dashboard:    http://localhost:8000
echo Simple View:  http://localhost:8000/simple.html
echo.
echo Press any key to exit (servers will keep running)
pause > nul
