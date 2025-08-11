# Load environment variables first
from dotenv import load_dotenv

load_dotenv()


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import screenshot, generate_code, home, evals, ollama_api

app = FastAPI(
    title="Website Builder API",
    description="AI-powered website builder with Ollama integration",
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

# Add routes - new Ollama API first for priority
app.include_router(ollama_api.router, prefix="/api/ollama", tags=["ollama"])
app.include_router(generate_code.router, prefix="/api", tags=["legacy"])
app.include_router(screenshot.router, prefix="/api", tags=["screenshot"])
app.include_router(home.router, prefix="/api", tags=["home"])
app.include_router(evals.router, prefix="/api", tags=["evaluations"])
