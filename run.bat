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

:: Dependencies must be installed explicitly before launch.

echo.
echo [INFO] Starting Web Link Scraper...
echo.

:: Prefer the project virtual environment when available.
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    python main.py
)

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with error code %errorlevel%.
    pause
)


