@echo off
title ANYTIME Contest - Setup Auto Start
color 0B

echo.
echo  █████╗ ███╗   ██╗██╗   ██╗████████╗██╗███╗   ███╗███████╗
echo ██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║████╗ ████║██╔════╝
echo ███████║██╔██╗ ██║ ╚████╔╝    ██║   ██║██╔████╔██║█████╗  
echo ██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██║██║╚██╔╝██║██╔══╝  
echo ██║  ██║██║ ╚████║   ██║      ██║   ██║██║ ╚═╝ ██║███████╗
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
echo.
echo                    Setup Auto Start
echo ============================================================
echo.

cd /d "%~dp0"

echo This will set up the server to start automatically when you turn on your PC.
echo.

set "startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "script_path=%~dp0start_server.bat"
set "startup_shortcut=%startup_folder%\ANYTIME_Contest.bat"

echo 📁 Source: %script_path%
echo 📁 Target: %startup_shortcut%
echo.

echo 🔄 Creating startup shortcut...
copy "%script_path%" "%startup_shortcut%"

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Auto-start has been configured!
    echo.
    echo 🎉 The server will now start automatically when you turn on your PC.
    echo.
    echo 📍 Your site will be available at:
    echo    • http://localhost:8000
    echo    • http://localhost:8000/docs (API documentation)
    echo    • http://localhost:8000/health (health check)
    echo    • admin_view.html (admin dashboard)
    echo.
    echo 🚀 You can also start the server manually by running:
    echo    start_server.bat
    echo.
) else (
    echo.
    echo ❌ FAILED to set up auto-start!
    echo.
    echo 💡 Try running this script as Administrator:
    echo    1. Right-click on this file
    echo    2. Select "Run as administrator"
    echo    3. Try again
    echo.
)

echo ============================================================
echo Press any key to exit...
echo ============================================================
pause >nul
