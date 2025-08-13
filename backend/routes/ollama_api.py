"""
Hardened, simplified API routes for local-only website generation.
"""
import logging
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
import re

from models.ollama_client import OllamaClient, OllamaConnectionError, OllamaModelError, ModelStatus
from services.prompt_manager import WebsitePromptManager
from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, REQUIRED_OLLAMA_MODELS, SHOULD_MOCK_AI_RESPONSE

logger = logging.getLogger(__name__)

router = APIRouter()

# --- Singleton Management ---

ollama_client_singleton: Optional[OllamaClient] = None

async def get_ollama_client() -> OllamaClient:
    """
    Dependency injection function to get the Ollama client singleton.
    Initializes the client on first call.
    """
    global ollama_client_singleton
    if ollama_client_singleton is None:
        try:
            ollama_client_singleton = OllamaClient(base_url=OLLAMA_BASE_URL)
            await ollama_client_singleton.initialize()
        except (OllamaConnectionError, OllamaModelError) as e:
            # This error will be caught by the health check on startup.
            # Logging it here is useful for debugging.
            logger.critical(f"Failed to initialize Ollama client: {e}")
            # The app won't be able to serve requests, but we don't raise here
            # to allow the health check endpoint to report the specific error.
    return ollama_client_singleton

# --- Pydantic Models ---

class GenerateWebsiteRequest(BaseModel):
    description: str = Field(..., description="A description of the website to generate.")
    model_name: str = Field(OLLAMA_MODEL_NAME, description="The Ollama model to use for generation.")

class GenerateWebsiteResponse(BaseModel):
    html: str
    css: str
    status: str = "success"

class HealthResponse(BaseModel):
    status: str
    ollama_url: str
    models: List[ModelStatus]

# --- API Endpoints ---

@router.get("/health", response_model=HealthResponse)
async def health_check(client: OllamaClient = Depends(get_ollama_client)):
    """
    Checks the connection to Ollama and verifies that required models are available.
    This endpoint is used by the frontend to determine if the app is ready.
    """
    if not client:
         raise HTTPException(
            status_code=503,
            detail="Ollama client could not be initialized. Check server logs for details."
        )
    try:
        # Re-run checks to get fresh status
        await client.initialize()
        return HealthResponse(
            status="healthy",
            ollama_url=OLLAMA_BASE_URL,
            models=client.model_status,
        )
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/generate/html", response_model=GenerateWebsiteResponse)
async def generate_website(
    request: GenerateWebsiteRequest,
    client: OllamaClient = Depends(get_ollama_client)
):
    """
    Generates a complete HTML page with CSS from a description, using a validated local model.
    """
    if SHOULD_MOCK_AI_RESPONSE:
        logger.info("SHOULD_MOCK_AI_RESPONSE is True, returning mock data.")
        mock_html = """<!DOCTYPE html><html lang="en"><head><title>Mock Page</title><link rel="stylesheet" href="style.css"></head><body><h1>Hello, Mock World!</h1></body></html>"""
        mock_css = """body { font-family: sans-serif; } h1 { color: blue; }"""
        return GenerateWebsiteResponse(html=mock_html, css=mock_css, status="success")

    if not client:
        raise HTTPException(status_code=503, detail="Application is not healthy. Cannot process requests.")

    if request.model_name not in REQUIRED_OLLAMA_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model requested. Only the following models are allowed: {', '.join(REQUIRED_OLLAMA_MODELS)}"
        )

    try:
        # The prompt manager now simply orchestrates the call.
        prompt_manager = WebsitePromptManager(client)
        generated_code = await prompt_manager.generate_website_from_description(
            description=request.description,
            model_name=request.model_name
        )
        
        return GenerateWebsiteResponse(
            html=generated_code.get("html", ""),
            css=generated_code.get("css", "")
        )
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Ollama service error during generation: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurred during website generation: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
