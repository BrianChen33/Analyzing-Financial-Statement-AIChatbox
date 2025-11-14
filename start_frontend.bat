@echo off
echo ========================================
echo 启动前端服务器
echo ========================================
echo.

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Node.js，请先安装Node.js 18+
    pause
    exit /b 1
)

echo [信息] Node.js版本:
node --version
echo.

REM 进入前端目录
cd frontend
if errorlevel 1 (
    echo [错误] 无法进入frontend目录
    pause
    exit /b 1
)

REM 检查node_modules
if not exist node_modules (
    echo [警告] 依赖未安装，正在安装...
    call npm install
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查.env.local
if not exist .env.local (
    echo [信息] 创建.env.local文件...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
)

echo [信息] 启动Next.js开发服务器...
echo [信息] 前端将在 http://localhost:3000 运行
echo [信息] 按 Ctrl+C 停止服务器
echo.
echo ========================================
echo.

call npm run dev

pause

