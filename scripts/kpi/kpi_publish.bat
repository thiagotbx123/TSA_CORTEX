@echo off
REM KPI Dashboard: rebuild + ensure ngrok is serving
REM Usage: double-click or run from terminal

echo ========================================
echo  KPI Dashboard - Rebuild ^& Publish
echo ========================================
echo.

REM 1. Run the full pipeline
echo [1/4] Running KPI pipeline...
cd /d C:\Users\adm_r\Tools\TSA_CORTEX\scripts\kpi
python orchestrate.py
if errorlevel 1 (
    echo [ERROR] Pipeline failed. Fix errors above and retry.
    pause
    exit /b 1
)
echo.

REM 2. Copy dashboard to dedicated serve folder (F01: never expose full Downloads)
echo [2/4] Preparing serve folder...
set SERVE_DIR=C:\Users\adm_r\Downloads\kpi-serve
if not exist "%SERVE_DIR%" mkdir "%SERVE_DIR%"
copy /Y "C:\Users\adm_r\Downloads\KPI_DASHBOARD.html" "%SERVE_DIR%\" >nul
echo Dashboard copied to %SERVE_DIR%

REM 3. Check if HTTP server is already running on port 8080
echo [3/4] Checking HTTP server on port 8080...
netstat -ano | findstr ":8080.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo Starting HTTP server...
    start /B "" python -m http.server 8080 --directory "%SERVE_DIR%" >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo HTTP server started on port 8080.
) else (
    echo HTTP server already running.
)
echo.

REM 4. Check if ngrok is already running
echo [4/4] Checking ngrok tunnel...
curl -s http://127.0.0.1:4040/api/tunnels >nul 2>&1
if errorlevel 1 (
    echo Starting ngrok...
    start /B "" ngrok http --url=uneffused-hoyt-unpunctually.ngrok-free.dev 8080 >nul 2>&1
    timeout /t 4 /nobreak >nul
    echo ngrok started.
) else (
    echo ngrok already running.
)
echo.

echo ========================================
echo  DONE! Dashboard is live at:
echo  https://uneffused-hoyt-unpunctually.ngrok-free.dev/KPI_DASHBOARD.html
echo ========================================
echo.
pause
