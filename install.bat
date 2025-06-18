@echo off
echo Installing CS2 External Cheat dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ and add it to your PATH.
    pause
    exit /b 1
)

REM Install pip if not available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Installing pip...
    python -m ensurepip --upgrade
)

REM Install requirements
echo Installing required packages...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Failed to install some packages.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

pip install cython setuptools wheel

echo.
echo Installation completed successfully!
echo You can now run the cheat by executing: python Main.py
echo.
pause
