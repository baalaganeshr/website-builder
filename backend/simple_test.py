import httpx
import asyncio

async def test_basic():
    print("Testing basic imports...")
    try:
        client = httpx.AsyncClient()
        response = await client.get("http://localhost:11434")
        print(f"Ollama status: {response.text}")
        await client.aclose()
        print("✅ Basic test passed!")
    except Exception as e:
        print(f"❌ Error: {e}")

asyncio.run(test_basic())
