#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from models.ollama_client import test_ollama_connection, stream_ollama_response

async def test_integration():
    print("Testing Ollama Integration...")
    print("=" * 40)
    
    # Test connection
    print("1. Testing Ollama connection...")
    is_connected = await test_ollama_connection()
    if is_connected:
        print("✅ Ollama connection successful!")
    else:
        print("❌ Ollama connection failed!")
        return
    
    # Test model streaming
    print("\n2. Testing model streaming...")
    test_prompt = "Hello! Can you help me create a simple HTML page?"
    
    print(f"Prompt: {test_prompt}")
    print("Response: ", end="", flush=True)
    
    async for chunk in stream_ollama_response(test_prompt):
        print(chunk, end="", flush=True)
    
    print("\n\n✅ Integration test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_integration())
