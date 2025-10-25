@echo off
echo 🚀 LandGen Development Server
echo ================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed
    echo Please install Python 3.9+ from https://www.python.org/
    exit /b 1
)

REM Check if .env.local exists
if not exist .env.local (
    echo ⚠️  Warning: .env.local not found
    echo Creating from template...
    copy .env.local.example .env.local
    echo ✅ Created .env.local - Please add your GEMINI_API_KEY
    echo.
)

REM Install dependencies if needed
if not exist node_modules (
    echo 📦 Installing frontend dependencies...
    call npm install
    echo.
)

if not exist api\__pycache__ (
    echo 📦 Installing backend dependencies...
    cd api
    pip install -r requirements.txt
    cd ..
    echo.
)

REM Start the dev servers
echo 🔥 Starting development servers...
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
echo Press Ctrl+C to stop
echo.

REM Enable Node.js deprecation traces for all child processes
set NODE_OPTIONS=--trace-deprecation

npm run dev:all

