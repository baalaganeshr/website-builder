# Only import what is needed for the simplified local-first setup
from .ollama_client import (
    OllamaClient,
    OllamaConnectionError,
    OllamaModelError,
    Completion,
    ChatMessage
)

# Re-export for easy access in other parts of the application
__all__ = [
    "OllamaClient",
    "OllamaConnectionError",
    "OllamaModelError",
    "Completion",
    "ChatMessage"
]
