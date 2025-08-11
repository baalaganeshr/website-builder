# Load environment variables first
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import ollama_api
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Website Builder API - Local Ollama Only",
    description="AI-powered website builder using local Ollama models",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS settings (frontend Vite default port)
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple request/response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️  {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"✅ {request.method} {request.url.path} -> {response.status_code}")
        return response
    except Exception as e:
        logger.exception(f"❌ Error handling {request.method} {request.url.path}: {e}")
        raise

# Add only the new Ollama API routes
app.include_router(ollama_api.router, prefix="/api/ollama", tags=["ollama"])

@app.get("/")
async def root():
    return {
        "message": "Website Builder API - Local Ollama Only",
    "docs": "/api/docs",
        "health": "/api/ollama/health",
        "models": ["gpt-oss-20b", "llama3.2:3b"],
        "endpoints": {
            "generate_html": "/api/ollama/generate/html",
            "generate_css": "/api/ollama/generate/css", 
            "generate_react": "/api/ollama/generate/react",
            "enhance_code": "/api/ollama/enhance",
            "fix_code": "/api/ollama/fix",
            "websocket": "/api/ollama/generate/stream"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "website-builder-local"}

# Test endpoint for frontend connectivity checks
@app.get("/api/test")
async def api_test():
    logger.info("/api/test called")
    return {"status": "ok", "message": "Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
