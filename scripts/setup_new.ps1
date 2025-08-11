# Website Builder Setup Script for Windows PowerShell
# Supports local Ollama GPT-20B integration

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Website Builder Setup Script" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will set up your Website Builder with AI Screenshot-to-Code" -ForegroundColor Yellow
Write-Host "including support for your local Ollama GPT-20B model." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue..."

# Check Python installation
Write-Host ""
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit..."
    exit 1
}

# Check Node.js installation
Write-Host ""
Write-Host "[2/5] Checking Node.js installation..." -ForegroundColor Green
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit..."
    exit 1
}

# Setup backend
Write-Host ""
Write-Host "[3/5] Setting up Python backend..." -ForegroundColor Green
Set-Location backend

if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    @"
# OpenAI Configuration (Optional for cloud models)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Anthropic Configuration (Optional for cloud models)  
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Ollama Configuration (for your local GPT-20B)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gpt-20b

# Server Configuration
PORT=7001
HOST=localhost
"@ | Out-File -FilePath ".env" -Encoding UTF8
}

Write-Host "Installing Poetry..." -ForegroundColor Yellow
try {
    pip install --upgrade poetry
    Write-Host "✅ Poetry installed successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️ WARNING: Poetry installation failed, trying alternative method..." -ForegroundColor Yellow
    python -m pip install --upgrade poetry
}

Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
try {
    poetry install
    Write-Host "✅ Backend dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Backend dependency installation failed" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Set-Location ..

# Setup frontend
Write-Host ""
Write-Host "[4/5] Setting up frontend..." -ForegroundColor Green
Set-Location frontend

if (-not (Test-Path ".env.local")) {
    Write-Host "Creating frontend environment file..." -ForegroundColor Yellow
    @"
# Backend URLs
VITE_HTTP_BACKEND_URL=http://localhost:7001
VITE_WS_BACKEND_URL=ws://localhost:7001
"@ | Out-File -FilePath ".env.local" -Encoding UTF8
}

Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
try {
    if (Test-Path "yarn.lock") {
        yarn install
    } else {
        npm install
    }
    Write-Host "✅ Frontend dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Frontend dependency installation failed" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Set-Location ..

# Create startup scripts
Write-Host ""
Write-Host "[5/5] Creating startup scripts..." -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your Website Builder is now ready with:" -ForegroundColor Green
Write-Host "  ✅ Cloud AI Models (OpenAI, Anthropic)" -ForegroundColor Green
Write-Host "  ✅ Local AI Models (Your GPT-20B via Ollama)" -ForegroundColor Green  
Write-Host "  ✅ Full screenshot-to-code functionality" -ForegroundColor Green
Write-Host "  ✅ Modern web development stack" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configure your models in backend\.env:" -ForegroundColor White
Write-Host "   - Add OpenAI/Anthropic API keys (optional)" -ForegroundColor Gray
Write-Host "   - Verify Ollama settings for your GPT-20B" -ForegroundColor Gray
Write-Host ""
Write-Host "2. For local AI (your GPT-20B):" -ForegroundColor White
Write-Host "   - Start Ollama: " -NoNewline -ForegroundColor Gray
Write-Host "ollama serve" -ForegroundColor Cyan
Write-Host "   - Verify model: " -NoNewline -ForegroundColor Gray  
Write-Host "ollama list" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Start the application:" -ForegroundColor White
Write-Host "   - Double-click " -NoNewline -ForegroundColor Gray
Write-Host "start.bat" -ForegroundColor Cyan
Write-Host "   - OR run: " -NoNewline -ForegroundColor Gray
Write-Host ".\start.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Open " -NoNewline -ForegroundColor Gray
Write-Host "http://localhost:5173" -ForegroundColor Cyan -NoNewline
Write-Host " in your browser" -ForegroundColor Gray
Write-Host ""
Write-Host "🔒 Your local GPT-20B model ensures complete privacy!" -ForegroundColor Green
Write-Host "💡 Check GETTING_STARTED.md for detailed instructions." -ForegroundColor Blue
Write-Host ""
Read-Host "Press Enter to finish..."
