@echo off
REM Appointment Booking System - Startup Script for Windows

echo.
echo ========================================
echo Appointment Booking System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

REM Check if database exists
if not exist "appointments.db" (
    echo Database will be created on first run.
)

REM Start the application
echo.
echo ========================================
echo Starting Appointment Booking System
echo ========================================
echo.
echo Server running at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
