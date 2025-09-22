@echo off
title Open Admin Dashboard
color 0B

echo.
echo  █████╗ ███╗   ██╗██╗   ██╗████████╗██╗███╗   ███╗███████╗
echo ██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██║████╗ ████║██╔════╝
echo ███████║██╔██╗ ██║ ╚████╔╝    ██║   ██║██╔████╔██║█████╗  
echo ██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██║██║╚██╔╝██║██╔══╝  
echo ██║  ██║██║ ╚████║   ██║      ██║   ██║██║ ╚═╝ ██║███████╗
echo ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
echo.
echo                    Opening Admin Dashboard
echo ============================================================
echo.

cd /d "%~dp0"

echo 🔄 Opening Admin Dashboard...
echo.

REM Try to open with default browser
start admin_view.html

echo ✅ Admin Dashboard opened in your default browser!
echo.
echo 📍 If the dashboard doesn't load properly:
echo    1. Make sure the server is running (start_server.bat)
echo    2. Check that http://localhost:8000 is accessible
echo    3. Try clicking "Sync Google Sheets" button
echo.

echo ============================================================
echo Press any key to exit...
echo ============================================================
pause >nul
