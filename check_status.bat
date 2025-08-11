@echo off
echo ========================================
echo   Website Builder Status Check
echo ========================================
echo.

echo [1] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo.
echo [2] Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found
    pause
    exit /b 1
)

echo.
echo [3] Checking Yarn...
yarn --version
if %errorlevel% neq 0 (
    echo ERROR: Yarn not found
    pause
    exit /b 1
)

echo.
echo [4] Checking Ollama...
curl -s http://localhost:11434 >nul
if %errorlevel% neq 0 (
    echo WARNING: Ollama not running - start with 'ollama serve'
) else (
    echo Ollama is running
)

echo.
echo [5] Checking available models...
ollama list

echo.
echo [6] Backend status...
curl -s http://localhost:7001 >nul
if %errorlevel% neq 0 (
    echo Backend not running - start with: cd backend && python -m uvicorn main:app --reload --port 7001
) else (
    echo Backend is running at http://localhost:7001
)

echo.
echo [7] Frontend status...
curl -s http://localhost:5173 >nul
if %errorlevel% neq 0 (
    echo Frontend not running - start with: cd frontend && yarn dev
) else (
    echo Frontend is running at http://localhost:5173
)

echo.
echo ========================================
echo   Status Check Complete
echo ========================================
echo.
echo To start the application:
echo 1. Make sure Ollama is running: ollama serve
echo 2. Start backend: cd backend && python -m uvicorn main:app --reload --port 7001
echo 3. Start frontend: cd frontend && yarn dev
echo 4. Open http://localhost:5173 in your browser
echo.
pause
