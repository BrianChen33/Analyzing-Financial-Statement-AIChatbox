@echo off
REM Quick start script for Financial Statement AI Chatbox (Windows)

echo ========================================
echo Financial Statement AI Chatbox Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo + Python found
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo + Virtual environment created
) else (
    echo + Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo + Dependencies installed successfully

REM Check for .env file
echo.
if not exist ".env" (
    echo ! No .env file found. Creating from template...
    copy .env.example .env
    echo + Created .env file. Please edit it and add your OpenAI API key.
    echo.
    echo To add your API key:
    echo   1. Get your key from: https://platform.openai.com/api-keys
    echo   2. Edit .env file and replace 'your-api-key-here' with your actual key
) else (
    echo + .env file exists
)

REM Create uploads directory
if not exist "uploads" mkdir uploads
echo + Uploads directory ready

REM Run tests
echo.
echo Running tests...
python -m pytest tests/ -v

if errorlevel 1 (
    echo X Tests failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo + Setup complete!
echo ========================================
echo.
echo Quick Start Options:
echo.
echo 1. Web Interface (Recommended):
echo    streamlit run app.py
echo.
echo 2. Command Line:
echo    python src/chatbot.py ^<path-to-pdf^>
echo.
echo 3. Run Examples:
echo    python examples/basic_usage.py
echo    python examples/advanced_analysis.py
echo.
echo 4. Run Tests:
echo    pytest tests/ -v
echo.

pause
