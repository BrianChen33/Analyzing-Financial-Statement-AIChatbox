@echo off
echo ========================================
echo Launch frontend server
echo ========================================
echo.

REM Check Node.js installation
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js 18+ is required. Please install it first.
    pause
    exit /b 1
)

echo [INFO] Node.js version:
node --version
echo.

REM Enter frontend directory
cd frontend
if errorlevel 1 (
    echo [ERROR] Unable to enter the frontend directory
    pause
    exit /b 1
)

REM Ensure node_modules exists
if not exist node_modules (
    echo [WARN] Dependencies missing, installing...
    call npm install
    if errorlevel 1 (
        echo [ERROR] Dependency installation failed
        pause
        exit /b 1
    )
)

REM Ensure .env.local exists
if not exist .env.local (
    echo [INFO] Creating .env.local...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
)

echo [INFO] Starting Next.js dev server...
echo [INFO] Frontend running at http://localhost:3000
echo [INFO] Press Ctrl+C to stop
echo.
echo ========================================
echo.

call npm run dev

pause

