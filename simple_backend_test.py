#!/usr/bin/env python3
"""
Simple test backend to verify Ollama integration works with the frontend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Simple Ollama backend test server running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "backend": "simple-test"}

@app.post("/generate-code")
async def test_generate_code():
    return {"status": "Ollama integration ready", "message": "Backend connected successfully!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7001)
