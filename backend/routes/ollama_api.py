"""
Simplified API routes for website generation using a local Ollama model.
"""

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from models.ollama_client import OllamaClient, OllamaConnectionError, OllamaModelError
from services.prompt_manager import WebsitePromptManager
from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, SUPPORTED_OLLAMA_MODELS

logger = logging.getLogger(__name__)

router = APIRouter()

# Globals for singletons
ollama_client: Optional[OllamaClient] = None
prompt_manager: Optional[WebsitePromptManager] = None

async def get_ollama_client() -> OllamaClient:
    """Get or create Ollama client singleton."""
    global ollama_client
    if ollama_client is None:
        ollama_client = OllamaClient(base_url=OLLAMA_BASE_URL)
        await ollama_client.check_connection()
    return ollama_client

async def get_prompt_manager() -> WebsitePromptManager:
    """Get or create prompt manager singleton."""
    global prompt_manager
    if prompt_manager is None:
        client = await get_ollama_client()
        prompt_manager = WebsitePromptManager(client)
    return prompt_manager

# Pydantic models for the simplified API
class GenerateWebsiteRequest(BaseModel):
    description: str = Field(..., description="A description of the website to generate.")
    model_name: Optional[str] = Field(OLLAMA_MODEL_NAME, description="The Ollama model to use for generation.")

class GenerateWebsiteResponse(BaseModel):
    html: str
    css: str
    status: str = "success"

class HealthResponse(BaseModel):
    status: str
    ollama_url: str
    available_models: list[str]
    supported_models: list[str]

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the API and the Ollama service are running."""
    try:
        client = await get_ollama_client()
        models = await client.list_models()
        return HealthResponse(
            status="healthy",
            ollama_url=OLLAMA_BASE_URL,
            available_models=models,
            supported_models=SUPPORTED_OLLAMA_MODELS,
        )
    except OllamaConnectionError as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Ollama connection error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during health check: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@router.post("/generate/html", response_model=GenerateWebsiteResponse)
async def generate_website(request: GenerateWebsiteRequest):
    """
    Generates a complete HTML page with CSS from a description.
    """
    try:
        manager = await get_prompt_manager()
        model_to_use = request.model_name or OLLAMA_MODEL_NAME
        
        # This is a new method I will need to implement in the prompt manager
        generated_code = await manager.generate_website_from_description(
            description=request.description,
            model_name=model_to_use
        )
        
        return GenerateWebsiteResponse(
            html=generated_code.get("html", ""),
            css=generated_code.get("css", "")
        )
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Ollama service error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating website: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate website.")
