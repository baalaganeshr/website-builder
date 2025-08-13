import httpx
import json

def run_e2e_test():
    url = "http://localhost:7001/api/ollama/generate/html"
    payload = {
        "description": "A simple landing page for a new app.",
        "model_name": "llama3.2:3b"
    }

    try:
        response = httpx.post(url, json=payload, timeout=300)
        response.raise_for_status()

        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

        data = response.json()
        if data.get("html") and data.get("css"):
            print("E2E Test Passed: Received HTML and CSS.")
        else:
            print("E2E Test Failed: Response did not contain HTML and CSS.")

    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(f"Response: {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    run_e2e_test()
