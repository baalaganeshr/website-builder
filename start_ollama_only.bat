@echo off
REM Start the Website Builder backend with Ollama-only routes
setlocal

cd /d "%~dp0backend"

REM Ensure required env vars are loaded from .env
if not exist .env (
  echo Warning: backend\.env not found. Using defaults.
)

REM Prefer uvicorn if installed
python -c "import uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
  echo Installing uvicorn...
  pip install uvicorn fastapi python-dotenv httpx pydantic websockets aiohttp >nul 2>&1
)

echo Starting backend on http://127.0.0.1:8000 (docs at /api/docs)
python -m uvicorn main_simple:app --host 127.0.0.1 --port 8000 --reload

endlocal