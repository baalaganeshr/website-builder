"""
Enhanced API routes for website generation using Ollama.
Provides clean, simple endpoints for the frontend to use.
"""

import logging
import asyncio
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel, Field
from models.ollama_client import OllamaClient, OllamaConnectionError, OllamaModelError
from services.prompt_manager import WebsitePromptManager
from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, SUPPORTED_OLLAMA_MODELS

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize Ollama client and prompt manager
ollama_client = None
prompt_manager = None

async def get_ollama_client() -> OllamaClient:
    """Get or create Ollama client singleton"""
    global ollama_client
    if ollama_client is None:
        ollama_client = OllamaClient(
            base_url=OLLAMA_BASE_URL
        )
        ollama_client.model_name = OLLAMA_MODEL_NAME  # Set model name as attribute
        await ollama_client.check_connection()
    return ollama_client

async def get_prompt_manager() -> WebsitePromptManager:
    """Get or create prompt manager singleton"""
    global prompt_manager
    if prompt_manager is None:
        client = await get_ollama_client()
        prompt_manager = WebsitePromptManager(client)
    return prompt_manager


# Pydantic models for API requests
class GenerateHTMLRequest(BaseModel):
    description: str = Field(..., description="Description of the HTML page to generate")
    additional_requirements: str = Field("", description="Additional requirements or constraints")
    model_name: Optional[str] = Field(None, description="Specific model to use (optional)")

class GenerateCSSRequest(BaseModel):
    mockup_description: str = Field(..., description="Description of the desired design")
    existing_html: str = Field("", description="Existing HTML code (optional)")
    model_name: Optional[str] = Field(None, description="Specific model to use (optional)")

class GenerateReactRequest(BaseModel):
    component_description: str = Field(..., description="Description of the React component")
    props: List[str] = Field(default_factory=list, description="Required props for the component")
    model_name: Optional[str] = Field(None, description="Specific model to use (optional)")

class EnhanceCodeRequest(BaseModel):
    existing_code: str = Field(..., description="Existing code to enhance")
    enhancement_request: str = Field(..., description="Description of enhancements needed")
    model_name: Optional[str] = Field(None, description="Specific model to use (optional)")

class FixCodeRequest(BaseModel):
    problematic_code: str = Field(..., description="Code with issues to fix")
    issues_description: str = Field(..., description="Description of the issues")
    model_name: Optional[str] = Field(None, description="Specific model to use (optional)")

class CreateWebsiteRequest(BaseModel):
    site_description: str = Field(..., description="Description of the website to create")
    pages: List[str] = Field(default_factory=list, description="List of pages needed")
    model_name: Optional[str] = Field(None, description="Specific model to use (optional)")

class ApiResponse(BaseModel):
    success: bool
    data: Any = None
    error: str = None


@router.get("/health")
async def health_check():
    """Check if the API and Ollama are working"""
    try:
        client = await get_ollama_client()
        models = await client.list_models()
        return ApiResponse(
            success=True,
            data={
                "status": "healthy",
                "ollama_url": OLLAMA_BASE_URL,
                "available_models": models,
                "supported_models": SUPPORTED_OLLAMA_MODELS
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return ApiResponse(success=False, error=str(e))


@router.post("/generate/html")
async def generate_html_page(request: GenerateHTMLRequest):
    """Generate HTML page from description"""
    try:
        manager = await get_prompt_manager()
        html_code = await manager.generate_html_page(
            description=request.description,
            additional_requirements=request.additional_requirements,
            model_name=request.model_name
        )
        return ApiResponse(success=True, data={"html": html_code})
    
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Ollama error: {e}")
        raise HTTPException(status_code=503, detail=f"Ollama service error: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating HTML: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/css")
async def generate_css_styles(request: GenerateCSSRequest):
    """Generate CSS styles from mockup description"""
    try:
        manager = await get_prompt_manager()
        css_code = await manager.generate_css_styles(
            mockup_description=request.mockup_description,
            existing_html=request.existing_html,
            model_name=request.model_name
        )
        return ApiResponse(success=True, data={"css": css_code})
    
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Ollama error: {e}")
        raise HTTPException(status_code=503, detail=f"Ollama service error: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating CSS: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/react")
async def generate_react_component(request: GenerateReactRequest):
    """Generate React component from description"""
    try:
        manager = await get_prompt_manager()
        react_code = await manager.generate_react_component(
            component_description=request.component_description,
            props=request.props,
            model_name=request.model_name
        )
        return ApiResponse(success=True, data={"react": react_code})
    
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Ollama error: {e}")
        raise HTTPException(status_code=503, detail=f"Ollama service error: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating React component: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enhance")
async def enhance_existing_code(request: EnhanceCodeRequest):
    """Enhance existing code based on request"""
    try:
        manager = await get_prompt_manager()
        enhanced_code = await manager.enhance_existing_code(
            existing_code=request.existing_code,
            enhancement_request=request.enhancement_request,
            model_name=request.model_name
        )
        return ApiResponse(success=True, data={"enhanced_code": enhanced_code})
    
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Ollama error: {e}")
        raise HTTPException(status_code=503, detail=f"Ollama service error: {str(e)}")
    except Exception as e:
        logger.error(f"Error enhancing code: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fix")
async def fix_code_issues(request: FixCodeRequest):
    """Fix issues in existing code"""
    try:
        manager = await get_prompt_manager()
        fixed_code = await manager.fix_code_issues(
            problematic_code=request.problematic_code,
            issues_description=request.issues_description,
            model_name=request.model_name
        )
        return ApiResponse(success=True, data={"fixed_code": fixed_code})
    
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Ollama error: {e}")
        raise HTTPException(status_code=503, detail=f"Ollama service error: {str(e)}")
    except Exception as e:
        logger.error(f"Error fixing code: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create/website")
async def create_full_website(request: CreateWebsiteRequest):
    """Create a complete multi-page website"""
    try:
        manager = await get_prompt_manager()
        website_files = await manager.create_full_website(
            site_description=request.site_description,
            pages=request.pages,
            model_name=request.model_name
        )
        return ApiResponse(success=True, data={"website_files": website_files})
    
    except (OllamaConnectionError, OllamaModelError) as e:
        logger.error(f"Ollama error: {e}")
        raise HTTPException(status_code=503, detail=f"Ollama service error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating website: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/generate/stream")
async def websocket_generate_stream(websocket: WebSocket):
    """WebSocket endpoint for streaming code generation"""
    await websocket.accept()
    
    try:
        manager = await get_prompt_manager()
        
        while True:
            # Receive request from client
            data = await websocket.receive_json()
            request_type = data.get("type")
            
            try:
                if request_type == "html":
                    await _stream_html_generation(websocket, manager, data)
                elif request_type == "css":
                    await _stream_css_generation(websocket, manager, data)
                elif request_type == "react":
                    await _stream_react_generation(websocket, manager, data)
                elif request_type == "enhance":
                    await _stream_code_enhancement(websocket, manager, data)
                elif request_type == "fix":
                    await _stream_code_fixing(websocket, manager, data)
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown request type: {request_type}"
                    })
                    
            except Exception as e:
                logger.error(f"Error processing {request_type}: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error processing {request_type}: {str(e)}"
                })
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")


async def _stream_html_generation(websocket: WebSocket, manager: WebsitePromptManager, data: Dict[str, Any]):
    """Stream HTML generation to WebSocket"""
    await websocket.send_json({"type": "status", "message": "Generating HTML..."})
    
    try:
        html_code = await manager.generate_html_page(
            description=data.get("description", ""),
            additional_requirements=data.get("additional_requirements", ""),
            model_name=data.get("model_name")
        )
        
        await websocket.send_json({
            "type": "complete",
            "data": {"html": html_code}
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error", 
            "message": f"HTML generation failed: {str(e)}"
        })


async def _stream_css_generation(websocket: WebSocket, manager: WebsitePromptManager, data: Dict[str, Any]):
    """Stream CSS generation to WebSocket"""
    await websocket.send_json({"type": "status", "message": "Generating CSS..."})
    
    try:
        css_code = await manager.generate_css_styles(
            mockup_description=data.get("mockup_description", ""),
            existing_html=data.get("existing_html", ""),
            model_name=data.get("model_name")
        )
        
        await websocket.send_json({
            "type": "complete",
            "data": {"css": css_code}
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"CSS generation failed: {str(e)}"
        })


async def _stream_react_generation(websocket: WebSocket, manager: WebsitePromptManager, data: Dict[str, Any]):
    """Stream React component generation to WebSocket"""
    await websocket.send_json({"type": "status", "message": "Generating React component..."})
    
    try:
        react_code = await manager.generate_react_component(
            component_description=data.get("component_description", ""),
            props=data.get("props", []),
            model_name=data.get("model_name")
        )
        
        await websocket.send_json({
            "type": "complete",
            "data": {"react": react_code}
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"React generation failed: {str(e)}"
        })


async def _stream_code_enhancement(websocket: WebSocket, manager: WebsitePromptManager, data: Dict[str, Any]):
    """Stream code enhancement to WebSocket"""
    await websocket.send_json({"type": "status", "message": "Enhancing code..."})
    
    try:
        enhanced_code = await manager.enhance_existing_code(
            existing_code=data.get("existing_code", ""),
            enhancement_request=data.get("enhancement_request", ""),
            model_name=data.get("model_name")
        )
        
        await websocket.send_json({
            "type": "complete",
            "data": {"enhanced_code": enhanced_code}
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"Code enhancement failed: {str(e)}"
        })


async def _stream_code_fixing(websocket: WebSocket, manager: WebsitePromptManager, data: Dict[str, Any]):
    """Stream code fixing to WebSocket"""
    await websocket.send_json({"type": "status", "message": "Fixing code issues..."})
    
    try:
        fixed_code = await manager.fix_code_issues(
            problematic_code=data.get("problematic_code", ""),
            issues_description=data.get("issues_description", ""),
            model_name=data.get("model_name")
        )
        
        await websocket.send_json({
            "type": "complete",
            "data": {"fixed_code": fixed_code}
        })
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": f"Code fixing failed: {str(e)}"
        })
