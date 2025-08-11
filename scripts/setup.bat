@echo off
echo.
echo ========================================
echo  Website Builder Setup Script
echo ========================================
echo.
echo This script will set up your Website Builder with AI Screenshot-to-Code
echo including support for your local Ollama GPT-20B model.
echo.
pause

echo.
echo [1/5] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo.
echo [2/5] Checking Node.js installation...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo.
echo [3/5] Setting up Python backend...
cd backend
if not exist .env (
    copy .env .env.backup 2>nul
    echo Creating .env file...
    (
        echo # OpenAI Configuration ^(Optional for cloud models^)
        echo OPENAI_API_KEY=sk-your-openai-api-key-here
        echo.
        echo # Anthropic Configuration ^(Optional for cloud models^)
        echo ANTHROPIC_API_KEY=your-anthropic-api-key-here
        echo.
        echo # Ollama Configuration ^(for your local GPT-20B^)
        echo OLLAMA_BASE_URL=http://localhost:11434
        echo OLLAMA_MODEL_NAME=gpt-20b
        echo.
        echo # Server Configuration
        echo PORT=7001
        echo HOST=localhost
    ) > .env
)

echo Installing Poetry...
pip install --upgrade poetry
if %errorlevel% neq 0 (
    echo WARNING: Poetry installation failed, trying alternative method...
    python -m pip install --upgrade poetry
)

echo Installing backend dependencies...
poetry install
if %errorlevel% neq 0 (
    echo ERROR: Backend dependency installation failed
    pause
    exit /b 1
)

cd ..

echo.
echo [4/5] Setting up frontend...
cd frontend

if not exist .env.local (
    echo Creating frontend environment file...
    (
        echo # Backend URLs
        echo VITE_HTTP_BACKEND_URL=http://localhost:7001
        echo VITE_WS_BACKEND_URL=ws://localhost:7001
    ) > .env.local
)

echo Installing frontend dependencies...
if exist yarn.lock (
    yarn install
) else (
    npm install
)

if %errorlevel% neq 0 (
    echo ERROR: Frontend dependency installation failed
    pause
    exit /b 1
)

cd ..

echo.
echo [5/5] Final setup...
echo Creating startup scripts...

REM Create start script
(
    echo @echo off
    echo echo Starting Website Builder with AI Screenshot-to-Code...
    echo echo.
    echo echo Starting Backend Server...
    echo start "Website Builder Backend" cmd /k "cd backend && poetry run uvicorn main:app --reload --port 7001"
    echo.
    echo echo Waiting for backend to initialize...
    echo timeout /t 3 /nobreak ^> nul
    echo.
    echo echo Starting Frontend Server...
    echo start "Website Builder Frontend" cmd /k "cd frontend && yarn dev"
    echo.
    echo echo.
    echo echo ✅ Both servers are starting...
    echo echo 🌐 Frontend will be available at: http://localhost:5173
    echo echo 🔧 Backend API will be available at: http://localhost:7001
    echo echo.
    echo echo For your local GPT-20B model:
    echo echo 1. Make sure Ollama is running: ollama serve
    echo echo 2. Verify your model: ollama list
    echo echo 3. Open http://localhost:5173 and select your local model!
    echo echo.
    echo pause
) > start.bat

echo.
echo ========================================
echo  ✅ SETUP COMPLETE!
echo ========================================
echo.
echo Your Website Builder is now ready with:
echo   ✅ Cloud AI Models (OpenAI, Anthropic)
echo   ✅ Local AI Models (Your GPT-20B via Ollama)
echo   ✅ Full screenshot-to-code functionality
echo   ✅ Modern web development stack
echo.
echo NEXT STEPS:
echo.
echo 1. Configure your models in backend\.env:
echo    - Add OpenAI/Anthropic API keys (optional)
echo    - Verify Ollama settings for your GPT-20B
echo.
echo 2. For local AI (your GPT-20B):
echo    - Start Ollama: ollama serve
echo    - Verify model: ollama list
echo.
echo 3. Start the application:
echo    - Double-click start.bat
echo    - OR run: start.bat
echo.
echo 4. Open http://localhost:5173 in your browser
echo.
echo 🔒 Your local GPT-20B model ensures complete privacy!
echo 💡 Check GETTING_STARTED.md for detailed instructions.
echo.
pause
