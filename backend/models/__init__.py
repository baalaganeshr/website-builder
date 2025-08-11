# Only import Ollama client since we're only using local models
from .ollama_client import stream_ollama_response, check_ollama_connection, OllamaClient, list_ollama_models
from llm import Completion

# Re-export the functions for backward compatibility
__all__ = [
    "stream_ollama_response",
    "check_ollama_connection", 
    "list_ollama_models",
    "OllamaClient",
    "Completion"
]
