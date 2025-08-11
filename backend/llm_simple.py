from enum import Enum
from typing import TypedDict


# Actual model versions that are passed to the LLMs and stored in our logs
class Llm(Enum):
    # Local Ollama model only
    OLLAMA_GPT_LOCAL = "gpt-oss:20b"


class Completion(TypedDict):
    duration: float
    code: str


# Explicitly map each model to the provider backing it.  This keeps provider
# groupings authoritative and avoids relying on name conventions when checking
# models elsewhere in the codebase.
MODEL_PROVIDER: dict[Llm, str] = {
    # Local Ollama model only
    Llm.OLLAMA_GPT_LOCAL: "ollama",
}

# Convenience sets for membership checks - only Ollama models now
OPENAI_MODELS = set()  # Empty - no OpenAI models
ANTHROPIC_MODELS = set()  # Empty - no Anthropic models  
GEMINI_MODELS = set()  # Empty - no Gemini models
OLLAMA_MODELS = {m for m, p in MODEL_PROVIDER.items() if p == "ollama"}
