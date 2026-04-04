import httpx
import asyncio
import json

async def test_mcp():
    print("--- [TRUTH CHECK] Attempting to talk to the NEW MCP server ---")
    url = "http://localhost:8000/call"
    payload = {
        "tool": "search_vector_store",
        "arguments": {
            "session_id": "test-session",
            "query": "hello"
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            print(f"Sending POST to {url}...")
            resp = await client.post(url, json=payload, timeout=30.0)
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text}")
            
            if resp.status_code == 200:
                print("\n✅ SUCCESS! The server is updated and healthy!")
            elif resp.status_code == 404:
                print("\n❌ FAILED: The server is NOT found at /call. It might still be the old version!")
            else:
                print(f"\n❌ FAILED: Received status {resp.status_code}")
                
    except Exception as e:
        print(f"\n❌ ERROR: Could not connect to the server: {e}")
        print("Is the server running on port 8000?")

if __name__ == "__main__":
    asyncio.run(test_mcp())
