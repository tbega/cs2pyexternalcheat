@echo off
title CS2 External Cheat - Installation Script
color 0A

echo ========================================
echo    CS2 External Cheat - Installer
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found - checking version...
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo [INFO] Python version: %pyver%
echo.

:: Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not available
    echo Please ensure pip is installed with Python
    echo.
    pause
    exit /b 1
)

echo [INFO] pip found - starting installation...
echo.

:: Upgrade pip first
echo [STEP 1/3] Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [WARNING] Failed to upgrade pip, continuing anyway...
)
echo.

:: Install wheel for better package compilation
echo [STEP 2/3] Installing wheel...
pip install wheel
echo.

:: Install requirements
echo [STEP 3/3] Installing required packages...
echo Installing from requirements.txt...

:: Install packages one by one with better error handling
echo.
echo Installing psutil...
pip install psutil
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install psutil
    goto :error
)

echo Installing pywin32...
pip install pywin32
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install pywin32
    goto :error
)

echo Installing requests...
pip install requests
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requests
    goto :error
)

echo Installing keyboard...
pip install keyboard
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install keyboard
    goto :error
)

echo Installing pynput...
pip install pynput
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install pynput
    goto :error
)

echo Installing dearpygui...
pip install dearpygui
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dearpygui
    goto :error
)

echo Installing pyMeow...
pip install pyMeow
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install pyMeow from pip
    echo [INFO] Trying alternative installation methods...
    
    :: Try installing from git if pip fails
    pip install git+https://github.com/qb-0/pyMeow
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install pyMeow from git as well
        echo Please install pyMeow manually or check if you have git installed
        goto :error
    )
)


echo.
echo ========================================
echo       Installation Complete!
echo ========================================
echo.
echo [SUCCESS] All packages installed successfully!
echo.
echo To run the cheat:
echo   1. Make sure Counter-Strike 2 is running
echo   2. Run as Administrator (recommended)
echo   3. Execute: python main.py
echo.
echo Important Notes:
echo - Run this program as Administrator for best compatibility
echo - Make sure CS2 is running before starting the cheat
echo - Some antivirus software may flag this as suspicious
echo - This is for educational purposes only
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo        Installation Failed!
echo ========================================
echo.
echo [ERROR] Installation encountered errors.
echo.
echo Troubleshooting steps:
echo 1. Make sure you're running as Administrator
echo 2. Check your internet connection
echo 3. Try running: python -m pip install --upgrade pip
echo 4. Install Visual C++ Redistributable if on Windows
echo 5. Try installing packages manually one by one
echo.
echo Manual installation commands:
echo   pip install psutil pywin32 requests keyboard pynput dearpygui
echo   pip install pyMeow
echo.
pause
exit /b 1