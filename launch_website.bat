@echo off
title ANYTIME Contest - Launch Website
color 0A

echo.
echo  █████╗ ███╗   ██╗██╗   ██╗████████╗██╗███╗   ███╗███████╗
echo ██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║████╗ ████║██╔════╝
echo ███████║██╔██╗ ██║ ╚████╔╝    ██║   ██║██╔████╔██║█████╗  
echo ██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██║██║╚██╔╝██║██╔══╝  
echo ██║  ██║██║ ╚████║   ██║      ██║   ██║██║ ╚═╝ ██║███████╗
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
echo.
echo                    Launch Website
echo ============================================================
echo.

cd /d "%~dp0"

echo 🔍 Checking if server is running...
netstat -an | findstr :8000 >nul
if %errorlevel% neq 0 (
    echo ⚠️  Server is not running on port 8000
    echo.
    echo 🚀 Starting server first...
    echo.
    start /min start_server.bat
    echo ⏳ Waiting for server to start...
    timeout /t 5 /nobreak >nul
) else (
    echo ✅ Server is already running on port 8000
)

echo.
echo 🌐 Opening website in browser...
echo.

REM Try multiple methods to open the browser
echo Method 1: Opening with default browser...
start index.html 2>nul
if %errorlevel% equ 0 (
    echo ✅ Successfully opened with default browser
    goto :success
)

echo Method 2: Opening with Chrome...
start chrome "file:///%CD%/index.html" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Successfully opened with Chrome
    goto :success
)

echo Method 3: Opening with Edge...
start msedge "file:///%CD%/index.html" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Successfully opened with Edge
    goto :success
)

echo Method 4: Opening with Firefox...
start firefox "file:///%CD%/index.html" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Successfully opened with Firefox
    goto :success
)

echo Method 5: Opening with Internet Explorer...
start iexplore "file:///%CD%/index.html" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Successfully opened with Internet Explorer
    goto :success
)

echo ❌ Could not open browser automatically
echo.
echo 💡 Manual steps:
echo    1. Open your web browser
echo    2. Navigate to: file:///%CD%/index.html
echo    3. Or go to: http://localhost:8000
echo.
goto :end

:success
echo.
echo 🎉 Website launched successfully!
echo.
echo 📍 Your contest is now available at:
echo    • Local file: file:///%CD%/index.html
echo    • Server URL: http://localhost:8000
echo    • Admin Dashboard: file:///%CD%/admin_view.html
echo.

:end
echo ============================================================
echo Press any key to exit...
echo ============================================================
pause >nul
