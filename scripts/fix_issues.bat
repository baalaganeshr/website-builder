@echo off
echo 🔧 Website Builder Issue Fix Script
echo ====================================

echo.
echo Step 1: Stopping any existing processes...
taskkill /F /IM ollama.exe 2>nul
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

echo.
echo Step 2: Starting Ollama server...
start /min "Ollama Server" ollama serve
echo Waiting for Ollama to initialize...
timeout /t 5 >nul

echo.
echo Step 3: Testing Ollama connection...
curl -s http://localhost:11434 >nul
if %errorlevel% equ 0 (
    echo ✅ Ollama server is running
) else (
    echo ❌ Ollama server failed to start
    echo Please check if Ollama is installed: https://ollama.ai
    pause
    exit /b 1
)

echo.
echo Step 4: Checking available models...
ollama list
echo.
echo If no models are available, install one with:
echo   ollama pull llama2
echo   ollama pull codellama
echo   ollama pull mistral

echo.
echo Step 5: Starting backend server...
cd /d "%~dp0backend"
start /min "Backend Server" cmd /c "python -m uvicorn main:app --reload --port 7001"
echo Waiting for backend to initialize...
timeout /t 5 >nul

echo.
echo Step 6: Testing backend connection...
curl -s http://localhost:7001 >nul
if %errorlevel% equ 0 (
    echo ✅ Backend server is running
) else (
    echo ❌ Backend server failed to start
    echo Check the Backend Server window for error details
)

echo.
echo Step 7: Starting frontend...
cd /d "%~dp0frontend"
start /min "Frontend Server" cmd /c "yarn dev"
echo Waiting for frontend to initialize...
timeout /t 3 >nul

echo.
echo ====================================
echo 🎉 Fix attempt complete!
echo ====================================
echo.
echo Check these URLs:
echo   Backend:  http://localhost:7001
echo   Frontend: http://localhost:5173
echo   Ollama:   http://localhost:11434
echo.
echo If you still see errors:
echo 1. Make sure you have a model installed: ollama pull llama2
echo 2. Add OpenAI API key to backend/.env for cloud models
echo 3. Check the Backend Server and Frontend Server windows for errors
echo.
echo Press any key to open the application...
pause >nul
start http://localhost:5173
