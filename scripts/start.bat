@echo off
echo 🚀 Starting Website Builder with AI Screenshot-to-Code...
echo.

echo 🔧 Starting Backend Server...
start "Backend" cmd /k "cd backend && C:/Users/baala/AppData/Local/Microsoft/WindowsApps/python3.13.exe -m poetry run uvicorn main:app --reload --port 7001"

echo ⏳ Waiting for backend to initialize...
timeout /t 3 /nobreak > nul

echo 🎨 Starting Frontend Server...
start "Frontend" cmd /k "cd frontend && yarn dev"

echo.
echo ✅ Both servers are starting...
echo 🌐 Frontend will be available at: http://localhost:5173
echo 🔧 Backend will be available at: http://localhost:7001
echo.
echo Press any key to exit...
pause > nul
