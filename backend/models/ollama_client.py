"""
Comprehensive Ollama client for local LLM integration with the website builder.
Supports streaming responses, multiple models, and robust error handling.
"""

import asyncio
import json
import time
from typing import AsyncGenerator, List, Dict, Any, Optional
import httpx

from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, SUPPORTED_OLLAMA_MODELS
from pydantic import BaseModel

class Completion(BaseModel):
    content: Optional[str] = None

class OllamaConnectionError(Exception):
    """Raised when Ollama server is not accessible"""
    pass


class OllamaModelError(Exception):
    """Raised when specified model is not available"""
    pass


# Generic message type for LLM interactions
ChatMessage = Dict[str, Any]


class OllamaClient:
    """Enhanced client for interacting with Ollama API with comprehensive error handling"""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, timeout: float = 300.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.model_name = OLLAMA_MODEL_NAME  # Default model name
        self.client = httpx.AsyncClient(timeout=timeout)
        self._available_models = None
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def check_connection(self) -> bool:
        """Check if Ollama server is running and accessible"""
        try:
            response = await self.client.get(f"{self.base_url}/api/version", timeout=5.0)
            return response.status_code == 200
        except Exception as e:
            print(f"Ollama connection check failed: {e}")
            return False
    
    async def list_models(self) -> List[str]:
        """Get list of available models from Ollama"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags", timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                models = [model["name"] for model in data.get("models", [])]
                self._available_models = models
                return models
            else:
                raise OllamaConnectionError(f"Failed to list models: {response.status_code}")
        except httpx.RequestError as e:
            raise OllamaConnectionError(f"Cannot connect to Ollama server: {e}")
    
    async def ensure_model_available(self, model_name: str) -> bool:
        """Ensure the specified model is available, with helpful error messages"""
        if not self._available_models:
            await self.list_models()
        
        if model_name not in self._available_models:
            available_str = ", ".join(self._available_models) if self._available_models else "none"
            error_msg = f"""
Model '{model_name}' not found in Ollama.
Available models: {available_str}

To install the model, run:
    ollama pull {model_name}

For the recommended models in this project, run:
    ollama pull llama3.1:3b
    ollama pull gpt-20b  # if available
"""
            raise OllamaModelError(error_msg)
        return True
    
    def _format_messages_for_ollama(self, messages: List[ChatMessage]) -> str:
        """
        Convert messages to a single prompt string for Ollama's /api/generate.
        """
        prompt_parts = []
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            # Basic handling for multimodal content, just extracting text
            if isinstance(content, list):
                text_content = " ".join(
                    item.get("text", "")
                    for item in content if isinstance(item, dict) and item.get("type") == "text"
                )
                content = text_content

            prompt_parts.append(f"### {role.capitalize()}\n{content}")

        # Add a final prompt for the assistant to start generating
        prompt_parts.append("### Assistant\n")
        return "\n\n".join(prompt_parts)

    async def generate_streaming_response(
        self,
        messages: List[ChatMessage],
        model_name: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming response from Ollama model with enhanced error handling
        """
        if not model_name:
            model_name = OLLAMA_MODEL_NAME
        
        # Validate connection and model availability
        if not await self.check_connection():
            raise OllamaConnectionError(
                "Cannot connect to Ollama server. Please ensure Ollama is running on " + 
                f"{self.base_url}. Start with: ollama serve"
            )
        
        await self.ensure_model_available(model_name)
        
        # Convert messages to Ollama format  
        prompt = self._format_messages_for_ollama(messages)
        
        print(f"Using Ollama model: {model_name}")
        
        # Prepare request payload
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens or 4096,  # Default to reasonable limit
                "stop": ["User:", "Human:"],  # Stop tokens to prevent confusion
            }
        }
        
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise OllamaConnectionError(
                        f"Ollama API error {response.status_code}: {error_text.decode()}"
                    )
                
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            data = json.loads(line)
                            
                            if data.get("error"):
                                raise OllamaConnectionError(f"Ollama error: {data['error']}")
                            
                            if "response" in data:
                                chunk = data["response"]
                                if chunk:  # Only yield non-empty chunks
                                    yield chunk
                            
                            # Check if generation is done
                            if data.get("done", False):
                                break
                                
                        except json.JSONDecodeError as e:
                            print(f"Failed to parse Ollama response: {line}")
                            continue
                            
        except httpx.TimeoutException:
            raise OllamaConnectionError(
                f"Timeout waiting for response from {model_name}. "
                "This might indicate the model is too large for your system or needs more time."
            )
        except httpx.RequestError as e:
            raise OllamaConnectionError(f"Network error communicating with Ollama: {e}")
    
    async def generate_completion(
        self,
        messages: List[ChatMessage],
        model_name: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None
    ) -> Completion:
        """
        Generate a complete (non-streaming) response from Ollama
        """
        full_response = ""
        async for chunk in self.generate_streaming_response(
            messages, model_name, temperature, max_tokens
        ):
            full_response += chunk
        
        return Completion(content=full_response)

    # This convenience wrapper is no longer needed with the new prompt manager
    # and can be removed. If streaming is needed again, it can be added back.
