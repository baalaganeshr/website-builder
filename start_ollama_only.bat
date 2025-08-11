@echo off
echo ========================================
echo   Starting Website Builder (Ollama Only)
echo ========================================

echo.
echo Step 1: Checking Ollama...
ollama list
echo.

echo Step 2: Starting Ollama server (if not running)...
start /min "Ollama Server" ollama serve
timeout /t 3 >nul

echo Step 3: Testing Ollama connection...
echo Testing gpt-oss:20b model...
ollama run gpt-oss:20b "Say 'Hello from your local GPT model!'" --verbose=false
if %errorlevel% neq 0 (
    echo.
    echo ❌ Model test failed. The model might be too large for your system.
    echo 💡 Try a smaller model: ollama pull llama3.2:1b
    echo 💡 Or ensure you have enough RAM (model needs ~13GB)
    pause
)

echo.
echo Step 4: Starting backend...
cd backend
start /min "Backend Server" cmd /k "python -m uvicorn main:app --reload --port 7001"
cd ..

echo.
echo Step 5: Starting frontend...
cd frontend
start /min "Frontend Server" cmd /k "yarn dev"
cd ..

echo.
echo ========================================
echo   ✅ Website Builder Started!
echo ========================================
echo.
echo Your local AI website builder is ready:
echo   🌐 Frontend: http://localhost:5173
echo   🔧 Backend:  http://localhost:7001
echo   🤖 Model:    gpt-oss:20b (Local/Private)
echo.
echo 🔒 Complete privacy - your data never leaves your machine!
echo.
echo Opening browser in 5 seconds...
timeout /t 5 >nul
start http://localhost:5173

echo.
pause
