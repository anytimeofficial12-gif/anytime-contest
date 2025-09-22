@echo off
title ANYTIME Contest Server
color 0A

echo.
echo  █████╗ ███╗   ██╗██╗   ██╗████████╗██╗███╗   ███╗███████╗
echo ██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║████╗ ████║██╔════╝
echo ███████║██╔██╗ ██║ ╚████╔╝    ██║   ██║██╔████╔██║█████╗  
echo ██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██║██║╚██╔╝██║██╔══╝  
echo ██║  ██║██║ ╚████║   ██║      ██║   ██║██║ ╚═╝ ██║███████╗
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
echo.
echo                    Contest Server
echo ============================================================
echo.

cd /d "%~dp0"

echo 🚀 Starting ANYTIME Contest Server...
echo 📁 Working directory: %CD%
echo 🕐 Started at: %date% %time%
echo.

REM Kill any existing Python processes on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a >nul 2>&1
)
timeout /t 2 /nobreak >nul

REM Start the server
python -m uvicorn app:app --host 0.0.0.0 --port 8000

echo.
echo ============================================================
echo Server stopped. Press any key to exit...
echo ============================================================
pause >nul
