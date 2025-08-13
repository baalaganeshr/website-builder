"""
Configuration file for the Local-Only AI Website Builder.

This file hardcodes the required settings to ensure the application runs in a
strictly local environment, connecting only to a local Ollama instance.
"""
import os

# --- Hardcoded Local Ollama Configuration ---
# The base URL for the local Ollama server. This is not configurable.
OLLAMA_BASE_URL = "http://localhost:11434"

# The specific local models required for this application to run.
REQUIRED_OLLAMA_MODELS = ["gpt-oss-20b", "llama3.2:3b"]

# The default model to use if none is specified by the frontend.
OLLAMA_MODEL_NAME = "llama3.2:3b"


# --- Deprecated or Unused Settings ---
# All cloud-based API keys and settings are removed to enforce local-only operation.
# Any logic attempting to use these should be removed or updated.

# --- Debugging-related ---
# For development and debugging purposes only.
IS_DEBUG_ENABLED = bool(os.environ.get("IS_DEBUG_ENABLED", False))
DEBUG_DIR = os.environ.get("DEBUG_DIR", "")
IS_PROD = False # This is a local-only application, so IS_PROD is always False.
SHOULD_MOCK_AI_RESPONSE = True # Mocks are enabled for testing without Ollama.
