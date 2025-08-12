"""
Hardened Ollama client for local-only LLM integration.

This client is specifically designed to work with a local Ollama instance
and a fixed set of required models. It performs strict checks on startup
to ensure the environment is correctly configured.
"""
import asyncio
import json
from typing import AsyncGenerator, List, Dict, Any, Optional
import httpx
from pydantic import BaseModel

from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, REQUIRED_OLLAMA_MODELS

# --- Data Models ---

class Completion(BaseModel):
    content: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: Any

class ModelStatus(BaseModel):
    name: str
    available: bool

# --- Custom Exceptions ---

class OllamaConnectionError(Exception):
    """Raised when the Ollama server is not accessible."""
    pass

class OllamaModelError(Exception):
    """Raised when a required model is not available in Ollama."""
    pass

# --- Ollama Client ---

class OllamaClient:
    """
    A client for interacting with a local Ollama API, hardened for local-only operation.
    It performs a connection check and model validation upon initialization.
    """
    def __init__(self, base_url: str = OLLAMA_BASE_URL, timeout: float = 300.0):
        if not base_url.startswith("http://localhost") and not base_url.startswith("http://127.0.0.1"):
            raise OllamaConnectionError(
                f"Security risk: OLLAMA_BASE_URL is not set to a local address. Got: {base_url}"
            )
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.model_name = OLLAMA_MODEL_NAME
        self.client = httpx.AsyncClient(timeout=timeout)
        self.model_status: List[ModelStatus] = []

    async def initialize(self):
        """
        Performs startup checks for connection and model availability.
        This must be called after creating an instance of the client.
        """
        await self._check_connection()
        await self._check_required_models()

    async def _check_connection(self):
        """
        Verifies that the Ollama server is running and accessible.
        Raises OllamaConnectionError if the connection fails.
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/version", timeout=5.0)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise OllamaConnectionError(
                "Cannot connect to Ollama server. Please ensure Ollama is running at "
                f"{self.base_url}. You can start it with: `ollama serve`"
            ) from e

    async def _check_required_models(self):
        """
        Checks if all models specified in REQUIRED_OLLAMA_MODELS are available.
        Populates `self.model_status` and raises OllamaModelError if any are missing.
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/tags", timeout=10.0)
            response.raise_for_status()
            data = response.json()
            available_models = {model["name"] for model in data.get("models", [])}

            missing_models = []
            for model_name in REQUIRED_OLLAMA_MODELS:
                is_available = model_name in available_models
                self.model_status.append(ModelStatus(name=model_name, available=is_available))
                if not is_available:
                    missing_models.append(model_name)

            if missing_models:
                missing_str = ", ".join(missing_models)
                raise OllamaModelError(
                    f"The following required models are not available in Ollama: {missing_str}. "
                    f"Please install them by running `ollama pull {model_name}` for each missing model."
                )
        except httpx.RequestError as e:
            raise OllamaConnectionError("Failed to list models from Ollama server.") from e
    
    async def list_models(self) -> List[ModelStatus]:
        """Returns the status of the required models."""
        return self.model_status

    def _format_messages_for_ollama(self, messages: List[ChatMessage]) -> str:
        """Converts messages to a single prompt string for Ollama's /api/generate."""
        prompt_parts = []
        for message in messages:
            prompt_parts.append(f"### {message.role.capitalize()}\n{message.content}")
        prompt_parts.append("### Assistant\n")
        return "\n\n".join(prompt_parts)

    async def generate_completion(
        self,
        messages: List[ChatMessage],
        model_name: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = 4096
    ) -> Completion:
        """
        Generates a complete (non-streaming) response from Ollama.
        """
        model_to_use = model_name or self.model_name
        if model_to_use not in REQUIRED_OLLAMA_MODELS:
            raise OllamaModelError(
                f"Model '{model_to_use}' is not an approved local model. "
                f"Please use one of: {', '.join(REQUIRED_OLLAMA_MODELS)}"
            )

        prompt = self._format_messages_for_ollama(messages)
        
        payload = {
            "model": model_to_use,
            "prompt": prompt,
            "stream": False,  # Non-streaming for this method
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "stop": ["User:", "Human:", "###"],
            }
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return Completion(content=data.get("response", ""))
        except httpx.TimeoutException as e:
            raise OllamaConnectionError(f"Timeout waiting for response from {model_to_use}.") from e
        except httpx.RequestError as e:
            raise OllamaConnectionError(f"Network error communicating with Ollama: {e}") from e

    async def close(self):
        """Closes the HTTP client."""
        await self.client.aclose()
