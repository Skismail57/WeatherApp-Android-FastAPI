"""
Test FastAPI route directly to see the actual error.
"""
import asyncio
import httpx

async def test_fastapi_route():
    """Test the FastAPI route directly."""
    print("Testing FastAPI route: http://127.0.0.1:8000/api/v1/weather/city/Bengaluru")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get("http://127.0.0.1:8000/api/v1/weather/city/Bengaluru")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"City: {data.get('city')}")
                print(f"Temperature: {data.get('temperature')}")
                print(f"Pressure: {data.get('pressure')}")
            else:
                print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fastapi_route())
