@echo off
echo ============================================================
echo    Mood Music App - Starting Web Server
echo ============================================================
echo.
cd /d "%~dp0"
echo Current directory: %CD%
echo.
echo Starting Flask server...
echo.
echo Your app will be available at:
echo   http://localhost:5000
echo   http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.
python app.py
pause

