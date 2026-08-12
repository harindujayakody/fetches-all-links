@echo off
title Web Link Scraper
cls

echo ===================================================
echo   ⚡ Web Link Scraper - Auto Launcher & Checker
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH!
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b %errorlevel%
)

:: Auto check and install missing modules from requirements.txt
echo [INFO] Checking Python dependencies...
python -m pip install -r requirements.txt --quiet --no-warn-script-location

echo.
echo [INFO] Starting Web Link Scraper...
echo.

:: Launch main script
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with error code %errorlevel%.
    pause
)
