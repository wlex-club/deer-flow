@echo off
echo 🦌 DeerFlow Backend Server Startup Script
echo ==========================================

REM Change to project directory
cd /d "E:\office-project\deer-flow"

REM Check if virtual environment exists
if not exist ".venv" (
    echo ❌ Virtual environment not found!
    echo Please run bootstrap.bat first to set up the environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in virtual environment!
    echo Please reinstall the virtual environment.
    pause
    exit /b 1
)

REM Check if server.py exists
if not exist "server.py" (
    echo ❌ server.py not found!
    echo Make sure you're in the correct directory.
    pause
    exit /b 1
)

REM Start the server
echo 🚀 Starting DeerFlow backend server...
echo 📍 Server will be available at: http://localhost:8000
echo 🔧 Press Ctrl+C to stop the server
echo.

uv run server.py --reload

REM If server exits, show message
echo.
echo 🛑 Server has stopped.
pause 