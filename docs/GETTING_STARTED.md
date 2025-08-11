# Getting Started with Website Builder

## Quick Start Guide for Local AI (Ollama + GPT-20B)

### 1. First-time Setup
Run the setup script to install all dependencies:
```powershell
./setup.ps1
```

### 2. Configure Environment
Edit `backend/.env` and set your Ollama configuration:
```env
# For your local GPT-20B model via Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=gpt-20b

# Optional: Cloud AI keys (leave empty to use only local)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

### 3. Start Ollama Server
Make sure your GPT-20B model is running:
```powershell
ollama serve
# In another terminal, verify your model:
ollama list
```

### 4. Start Development Servers
Double-click `start.bat` or run:
```powershell
./start.bat
```

This will start both the backend and frontend servers automatically.

### 5. Open the Application
Open your browser and go to: <http://localhost:5173>

## What You Can Do with Local AI

1. **Upload a Screenshot**: Drag and drop any image of a website, mockup, or design
2. **Choose Output Format**: Select React, Vue, HTML, or other frameworks  
3. **Select Ollama Model**: Choose your local GPT-20B model for generation
4. **Generate Code**: Click generate and watch your local AI create functional code
5. **Preview & Edit**: See live preview and edit the code in real-time
6. **Export**: Download your generated website

## Benefits of Local AI

- **🔒 Privacy**: Your data never leaves your machine
- **💰 Cost-effective**: No API usage fees
- **⚡ Fast**: Direct local inference (depending on your hardware)
- **🌐 Offline**: Works without internet connection
- **🎛️ Control**: Full control over the AI model and parameters

## Troubleshooting

### Ollama Issues
- **"Cannot connect to Ollama server"**: Make sure `ollama serve` is running
- **"Model not found"**: Run `ollama list` to see available models, then `ollama pull gpt-20b` if needed
- **Slow generation**: This is normal for large models on CPU. Consider using GPU acceleration if available.

### Backend Issues
- Check `backend/.env` has correct `OLLAMA_BASE_URL` and `OLLAMA_MODEL_NAME`
- Ensure port 11434 is not blocked by firewall
- Look at backend console output for detailed error messages

## Advanced Configuration

You can customize the Ollama integration in `backend/.env`:

```env
# Change Ollama server URL (if running on different host/port)
OLLAMA_BASE_URL=http://192.168.1.100:11434

# Use a different model name
OLLAMA_MODEL_NAME=your-custom-model

# Mix local and cloud models (the UI will show all available options)
OPENAI_API_KEY=sk-your-key-here
OLLAMA_BASE_URL=http://localhost:11434
```

## Need Help?

- Check the main `README.md` for detailed documentation
- Look at `Troubleshooting.md` for common issues
- Your local setup logs appear in the backend console
