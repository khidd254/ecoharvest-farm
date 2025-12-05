#!/bin/bash

# Appointment Booking System - Startup Script for macOS/Linux

echo ""
echo "========================================"
echo "Appointment Booking System"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Check if database exists
if [ ! -f "appointments.db" ]; then
    echo "Database will be created on first run."
fi

# Start the application
echo ""
echo "========================================"
echo "Starting Appointment Booking System"
echo "========================================"
echo ""
echo "Server running at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
