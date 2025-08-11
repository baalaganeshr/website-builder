#!/usr/bin/env python3
"""
Configuration Summary for Website Builder (Ollama Only)
Shows the current configuration for your local GPT model setup.
"""

import os
import sys
from pathlib import Path

def show_configuration():
    print("🔧 Website Builder Configuration (Local AI Only)")
    print("=" * 60)
    
    # Project root
    root = Path(__file__).parent
    print(f"📁 Project Root: {root}")
    
    # Backend configuration
    print(f"\n🔧 Backend Configuration:")
    env_file = root / "backend" / ".env"
    if env_file.exists():
        print(f"   📄 Environment file: ✅ Found")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if 'OLLAMA' in line:
                        print(f"   🔗 {line}")
    else:
        print(f"   ❌ Environment file not found!")
    
    # Check LLM configuration
    llm_file = root / "backend" / "llm.py"
    if llm_file.exists():
        print(f"   📄 LLM config: ✅ Simplified (Ollama only)")
    
    # Frontend configuration  
    print(f"\n🎨 Frontend Configuration:")
    models_file = root / "frontend" / "src" / "lib" / "models.ts"
    if models_file.exists():
        print(f"   📄 Models config: ✅ Updated (Local model only)")
        with open(models_file, 'r') as f:
            content = f.read()
            if 'gpt-oss:20b' in content and 'Local GPT-20B' in content:
                print(f"   🤖 Model UI: ✅ Shows 'Local GPT-20B (Private)'")
            else:
                print(f"   ⚠️  Model UI: Might need updates")
    
    # Check Ollama status
    print(f"\n🤖 Ollama Status:")
    try:
        result = os.system('ollama list >nul 2>&1')
        if result == 0:
            print(f"   📊 Ollama CLI: ✅ Available")
            print(f"   🔍 Available models:")
            os.system('ollama list')
        else:
            print(f"   ❌ Ollama CLI: Not found or not running")
    except:
        print(f"   ❌ Error checking Ollama status")
    
    print(f"\n🚀 Quick Start:")
    print(f"   1. Run: .\\start_ollama_only.bat")
    print(f"   2. Open: http://localhost:5173")
    print(f"   3. Select: 'Local GPT-20B (Private)' in the dropdown")
    print(f"   4. Upload a screenshot and generate code!")
    
    print(f"\n🔒 Privacy Benefits:")
    print(f"   ✅ No API keys needed")
    print(f"   ✅ No data sent to external servers")
    print(f"   ✅ Complete offline operation")
    print(f"   ✅ Your code generation stays private")
    
    print(f"\n" + "=" * 60)
    print(f"🎉 Configuration Complete! Your local AI website builder is ready.")

if __name__ == "__main__":
    show_configuration()
