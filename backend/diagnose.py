#!/usr/bin/env python3
"""
Diagnostic script to identify issues with the Website Builder setup
"""

import sys
import os
import json
import asyncio
import subprocess
from pathlib import Path

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent))

try:
    import httpx
    from dotenv import load_dotenv
    print("✅ Basic imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Load environment variables
load_dotenv()

async def diagnose_issues():
    print("🔍 Website Builder Diagnostic Report")
    print("=" * 50)
    
    # 1. Check environment variables
    print("\n1. Environment Variables:")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model_name = os.getenv("OLLAMA_MODEL_NAME", "")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    
    print(f"   OLLAMA_BASE_URL: {ollama_base_url}")
    print(f"   OLLAMA_MODEL_NAME: {ollama_model_name}")
    print(f"   OPENAI_API_KEY: {'Set' if openai_api_key.startswith('sk-') else 'Not set or invalid'}")
    
    # 2. Check Ollama server
    print("\n2. Ollama Server Status:")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(ollama_base_url)
            if response.status_code == 200:
                print("   ✅ Ollama server is running")
            else:
                print(f"   ❌ Ollama server returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cannot connect to Ollama server: {e}")
        print("   💡 Solution: Start Ollama with 'ollama serve'")
    
    # 3. Check available models
    print("\n3. Available Ollama Models:")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            models = result.stdout.strip()
            if models and "NAME" in models:
                print("   ✅ Models found:")
                for line in models.split('\n')[1:]:  # Skip header
                    if line.strip():
                        print(f"      - {line.strip()}")
            else:
                print("   ⚠️ No models available")
                print("   💡 Solution: Pull a model with 'ollama pull llama2' or similar")
        else:
            print(f"   ❌ Error listing models: {result.stderr}")
    except FileNotFoundError:
        print("   ❌ Ollama CLI not found")
        print("   💡 Solution: Install Ollama from https://ollama.ai")
    except subprocess.TimeoutExpired:
        print("   ❌ Ollama command timed out")
    except Exception as e:
        print(f"   ❌ Error checking models: {e}")
    
    # 4. Check backend server
    print("\n4. Backend Server Status:")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:7001")
            if response.status_code == 200:
                print("   ✅ Backend server is running")
            else:
                print(f"   ❌ Backend server returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cannot connect to backend server: {e}")
        print("   💡 Solution: Start backend with 'python -m uvicorn main:app --reload --port 7001'")
    
    # 5. Test model inference (if Ollama is available)
    print("\n5. Model Inference Test:")
    if ollama_model_name:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                test_request = {
                    "model": ollama_model_name,
                    "prompt": "Hello! Please respond with 'Test successful'",
                    "stream": False
                }
                response = await client.post(
                    f"{ollama_base_url}/api/generate",
                    json=test_request
                )
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Model {ollama_model_name} is working")
                    print(f"   Response: {result.get('response', 'No response')[:50]}...")
                else:
                    print(f"   ❌ Model test failed with status {response.status_code}")
                    print(f"   Error: {response.text[:100]}...")
        except Exception as e:
            print(f"   ❌ Model test failed: {e}")
    else:
        print("   ⚠️ No model name configured")
    
    # 6. Recommendations
    print("\n6. Recommendations:")
    print("   📋 To fix common issues:")
    print("      1. Start Ollama: ollama serve")
    print("      2. Pull a model: ollama pull llama2")
    print("      3. Start backend: cd backend && python -m uvicorn main:app --reload --port 7001")
    print("      4. Start frontend: cd frontend && yarn dev")
    print("      5. Add OpenAI API key to .env if you want to use cloud models")
    
    print("\n" + "=" * 50)
    print("🏁 Diagnostic Complete")

if __name__ == "__main__":
    asyncio.run(diagnose_issues())
