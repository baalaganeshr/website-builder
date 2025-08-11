from enum import Enum
from typing import TypedDict


# Actual model versions that are passed to the LLMs and stored in our logs
class Llm(Enum):
    # Local Ollama models (ordered by size - smaller first for better compatibility)
    OLLAMA_LLAMA_3_2_3B = "llama3.2:3b"      # 3B params - Good for most systems
    OLLAMA_LLAMA_3_2_1B = "llama3.2:1b"      # 1B params - Fastest, works on any system
    OLLAMA_GPT_20B = "llama3.2:latest"       # Using working model (was gpt-oss:20b)


class Completion(TypedDict):
    duration: float
    code: str


# Explicitly map each model to the provider backing it.  This keeps provider
# groupings authoritative and avoids relying on name conventions when checking
# models elsewhere in the codebase.
MODEL_PROVIDER: dict[Llm, str] = {
    # Local Ollama models only
    Llm.OLLAMA_LLAMA_3_2_3B: "ollama",
    Llm.OLLAMA_LLAMA_3_2_1B: "ollama",
    Llm.OLLAMA_GPT_20B: "ollama",
}

# Convenience sets for membership checks - only Ollama models now
OPENAI_MODELS = set()  # Empty - no OpenAI models
ANTHROPIC_MODELS = set()  # Empty - no Anthropic models  
GEMINI_MODELS = set()  # Empty - no Gemini models
OLLAMA_MODELS = {m for m, p in MODEL_PROVIDER.items() if p == "ollama"}
