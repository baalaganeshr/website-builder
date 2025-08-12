# Load environment variables first
from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import ollama_api

app = FastAPI(
    title="Local Website Builder API",
    description="A local-first AI website builder using Ollama.",
    version="1.0.0",
    openapi_url="/api/openapi.json" if not __import__("config").IS_PROD else None,
    docs_url="/api/docs" if not __import__("config").IS_PROD else None,
    redoc_url="/api/redoc" if not __import__("config").IS_PROD else None,
)

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the simplified Ollama API router
app.include_router(ollama_api.router, prefix="/api/ollama", tags=["Ollama"])
