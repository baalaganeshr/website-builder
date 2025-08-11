#!/usr/bin/env python3
"""
Test script to verify Ollama integration with the website builder.
Run this to test if your local GPT-20B model is accessible.
"""

import asyncio
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.append('backend')

# Import directly from ollama_client to avoid dependency issues
from models.ollama_client import OllamaClient, stream_ollama_response, check_ollama_connection
from llm import Completion
from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME


async def test_ollama_integration():
    print("🧪 Testing Ollama Integration for Website Builder")
    print("=" * 50)
    
    # Test 1: Check connection
    print(f"1. Testing connection to Ollama at {OLLAMA_BASE_URL}...")
    is_connected = await check_ollama_connection()
    if is_connected:
        print("   ✅ Ollama server is running and accessible!")
    else:
        print("   ❌ Cannot connect to Ollama server!")
        print("   💡 Make sure to run: ollama serve")
        return False
    
    # Test 2: Check if the configured model exists
    print(f"\n2. Testing model '{OLLAMA_MODEL_NAME}' with simple generation...")
    
    try:
        # Use the OllamaClient with proper async handling
        client = OllamaClient()
        test_messages = [
            {
                "role": "user", 
                "content": "Hello, respond with 'Model test successful'"
            }
        ]
        
        print("   Generating response... (this may take a moment)")
        response = ""
        async for chunk in client.generate_streaming_response(
            messages=test_messages,
            model_name=OLLAMA_MODEL_NAME,
            temperature=0.0,
            max_tokens=50
        ):
            response += chunk
            print(chunk, end='', flush=True)
        
        if response.strip():
            print(f"\n   ✅ Model '{OLLAMA_MODEL_NAME}' is working!")
            print(f"   📝 Generated {len(response)} characters")
        else:
            print(f"\n   ❌ Model '{OLLAMA_MODEL_NAME}' did not respond!")
            return False
            
        await client.close()
            
    except Exception as e:
        print(f"\n   ❌ Error testing model: {e}")
        print(f"   💡 Make sure the model is available: ollama pull {OLLAMA_MODEL_NAME}")
        import traceback
        print("   Full error traceback:")
        traceback.print_exc()
        return False
    
    # Test 3: Test simple generation
    print(f"\n3. Testing code generation with {OLLAMA_MODEL_NAME}...")
    test_messages = [
        {
            "role": "system", 
            "content": "You are an expert web developer. Generate clean, working HTML code."
        },
        {
            "role": "user", 
            "content": "Create a simple HTML page with a blue header saying 'Hello World' and a paragraph with some text."
        }
    ]
    
    try:
        print("   Generating code... (this may take a moment)")
        
        async def print_chunk(chunk):
            print(chunk, end='', flush=True)
        
        completion = await stream_ollama_response(
            messages=test_messages,
            model_name=OLLAMA_MODEL_NAME,
            temperature=0.0,
            max_tokens=500,
            callback=print_chunk
        )
        
        print(f"\n   ✅ Generation completed in {completion['duration']:.2f} seconds!")
        print(f"   📊 Generated {len(completion['code'])} characters of code")
        
    except Exception as e:
        print(f"   ❌ Error during generation: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Your Ollama integration is ready!")
    print("\nNext steps:")
    print("1. Start the backend: cd backend && poetry run uvicorn main:app --reload --port 7001")
    print("2. Start the frontend: cd frontend && yarn dev")
    print("3. Open http://localhost:5173 and select your local model!")
    
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_ollama_integration())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
