#!/usr/bin/env python3
"""
Quick diagnostic to verify the fixes
"""

import asyncio
import subprocess
import httpx

async def quick_test():
    print("🔍 Quick Fix Verification")
    print("=" * 30)
    
    # 1. Check Ollama models
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama models available:")
            print(result.stdout)
        else:
            print("❌ No Ollama models found")
            print("💡 Install with: ollama pull llama2")
    except:
        print("❌ Ollama not available")
        print("💡 Start with: ollama serve")
    
    # 2. Test Ollama connection
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434")
            if response.status_code == 200:
                print("✅ Ollama server is running")
            else:
                print("❌ Ollama server not responding")
    except:
        print("❌ Cannot connect to Ollama")
        print("💡 Start with: ollama serve")
    
    # 3. Test backend
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:7001")
            if response.status_code == 200:
                print("✅ Backend server is running")
                
                # Test the code generation endpoint
                try:
                    ws_url = "ws://localhost:7001/generate-code"
                    print(f"💡 Use WebSocket at: {ws_url}")
                except:
                    pass
            else:
                print("❌ Backend server not responding")
    except:
        print("❌ Backend not available")
        print("💡 Start with: cd backend && python -m uvicorn main:app --reload --port 7001")
    
    print("\n🎯 Next steps:")
    print("1. Make sure Ollama is running: ollama serve")
    print("2. Install a model if needed: ollama pull llama2")
    print("3. Start backend: cd backend && python -m uvicorn main:app --reload --port 7001")
    print("4. Start frontend: cd frontend && yarn dev")

if __name__ == "__main__":
    asyncio.run(quick_test())
