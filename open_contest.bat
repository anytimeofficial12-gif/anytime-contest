@echo off
title Open ANYTIME Contest
color 0A

echo.
echo  █████╗ ███╗   ██╗██╗   ██╗████████╗██╗███╗   ███╗███████╗
echo ██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║████╗ ████║██╔════╝
echo ███████║██╔██╗ ██║ ╚████╔╝    ██║   ██║██╔████╔██║█████╗  
echo ██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██║██║╚██╔╝██║██╔══╝  
echo ██║  ██║██║ ╚████║   ██║      ██║   ██║██║ ╚═╝ ██║███████╗
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
echo.
echo                    Opening Contest Page
echo ============================================================
echo.

cd /d "%~dp0"

echo 🔄 Opening ANYTIME Contest page...
echo.

REM Try to open with default browser
start index.html

echo ✅ Contest page opened in your default browser!
echo.
echo 📍 If the page doesn't load properly:
echo    1. Make sure the server is running (start_server.bat)
echo    2. Check that http://localhost:8000 is accessible
echo    3. Try refreshing the page
echo.

echo ============================================================
echo Press any key to exit...
echo ============================================================
pause >nul
