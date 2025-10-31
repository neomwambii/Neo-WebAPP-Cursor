@echo off
echo Starting PowerBall Predictor...
echo.

REM Try to find Python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python found, starting application...
    python app.py
) else (
    echo Python not found in PATH. Trying py command...
    py --version >nul 2>&1
    if %errorlevel% == 0 (
        echo Python found via py command, starting application...
        py app.py
    ) else (
        echo Python not found. Please install Python and add it to your PATH.
        echo You can download Python from https://www.python.org/downloads/
        pause
    )
)

