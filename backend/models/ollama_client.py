"""
Ollama client for local LLM integration with the website builder.
Supports streaming responses and vision capabilities through Ollama API.
"""

import asyncio
import json
import time
from typing import AsyncGenerator, List, Dict, Any, Optional
import httpx
from openai.types.chat import ChatCompletionMessageParam

from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME
from llm import Completion
from utils import print_prompt_summary


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=300.0)  # 5 minute timeout for long responses
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    def _format_messages_for_ollama(self, messages: List[ChatCompletionMessageParam]) -> str:
        """
        Convert OpenAI-style messages to a single prompt string for Ollama.
        Ollama typically works with a single prompt rather than message arrays.
        """        
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if isinstance(content, list):
                # Handle multimodal content (text + images)
                text_parts = []
                for item in content:
                    if isinstance(item, dict):
                        if item.get("type") == "text":
                            text_parts.append(item.get("text", ""))
                        elif item.get("type") == "image_url":
                            # For now, we'll include a placeholder for images
                            # Ollama vision models would need special handling
                            text_parts.append("[IMAGE PROVIDED]")
                content = " ".join(text_parts)
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        # Add final instruction for the assistant to respond
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)
    
    async def generate_streaming_response(
        self,
        messages: List[ChatCompletionMessageParam],
        model_name: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming response from Ollama model
        """
        if not model_name:
            model_name = OLLAMA_MODEL_NAME
        
        # Convert messages to Ollama format
        prompt = self._format_messages_for_ollama(messages)
        
        # Print prompt summary for debugging (pass original messages, not the formatted prompt)
        print_prompt_summary(messages)
        
        # Prepare request payload
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
            }
        }
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            if "response" in chunk:
                                yield chunk["response"]
                            
                            # Check if generation is done
                            if chunk.get("done", False):
                                break
                                
                        except json.JSONDecodeError:
                            # Skip malformed JSON lines
                            continue
                            
        except httpx.HTTPError as e:
            print(f"Ollama API error: {e}")
            yield f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            yield f"Unexpected error: {str(e)}"


# Global client instance
ollama_client = OllamaClient()


async def stream_ollama_response(
    messages: List[ChatCompletionMessageParam],
    model_name: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
    callback: Optional[callable] = None
) -> Completion:
    """
    Stream response from Ollama model and return completion data
    """
    start_time = time.time()
    full_response = ""
    
    try:
        async for chunk in ollama_client.generate_streaming_response(
            messages=messages,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        ):
            full_response += chunk
            if callback:
                await callback(chunk)
        
        # Calculate duration and return completion data
        duration = time.time() - start_time
        return Completion(duration=duration, code=full_response)
        
    except Exception as e:
        print(f"Error in stream_ollama_response: {e}")
        error_response = f"Error: {str(e)}"
        if callback:
            await callback(error_response)
        
        duration = time.time() - start_time
        return Completion(duration=duration, code=error_response)


async def check_ollama_connection(base_url: str = OLLAMA_BASE_URL) -> bool:
    """
    Check if Ollama server is running and accessible
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{base_url}/api/tags")
            return response.status_code == 200
    except:
        return False


async def list_ollama_models(base_url: str = OLLAMA_BASE_URL) -> List[Dict[str, Any]]:
    """
    List available models in Ollama
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return data.get("models", [])
    except:
        pass
    return []


# Cleanup function to close the client
async def cleanup_ollama_client():
    """Close the Ollama client connection"""
    await ollama_client.close()
