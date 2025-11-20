@echo off
echo ========================================
echo Launch backend server
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8 or newer.
    pause
    exit /b 1
)

echo [INFO] Python version:
python --version
echo.

REM Dependency check
echo [INFO] Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [WARN] Dependencies missing, installing...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed
        pause
        exit /b 1
    )
)

echo [INFO] Dependencies ready
echo.

REM Check .env file
if not exist .env (
    echo [WARN] .env file not found
    echo [TIP] Create .env and add your TONGYI_API_KEY
    echo.
)

REM Start server
echo [INFO] Starting FastAPI server...
echo [INFO] Server running at http://localhost:8000
echo [INFO] Press Ctrl+C to stop
echo.
echo ========================================
echo.

python api_server.py

pause

