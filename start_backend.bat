@echo off
echo ========================================
echo 启动后端服务器
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [信息] Python版本:
python --version
echo.

REM 检查依赖
echo [信息] 检查依赖...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [警告] 依赖未安装，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [信息] 依赖检查完成
echo.

REM 检查.env文件
if not exist .env (
    echo [警告] 未找到.env文件
    echo [提示] 请创建.env文件并添加OPENAI_API_KEY
    echo.
)

REM 启动服务器
echo [信息] 启动FastAPI服务器...
echo [信息] 服务器将在 http://localhost:8000 运行
echo [信息] 按 Ctrl+C 停止服务器
echo.
echo ========================================
echo.

python api_server.py

pause

