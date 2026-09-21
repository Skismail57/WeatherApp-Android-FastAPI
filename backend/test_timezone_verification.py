import httpx
import asyncio
import json

BASE_URL = "http://127.0.0.1:8000"

cities = [
    "Bengaluru",
    "London",
    "New York",
    "Sydney",
    "Dubai"
]

async def test_city(city):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/api/v1/weather/city/{city}/forecast")
            if response.status_code == 200:
                data = response.json()
                print(f"\n{'='*60}")
                print(f"City: {city}")
                print(f"{'='*60}")
                print(f"Timezone ID: {data.get('timezone_id', 'N/A')}")
                print(f"Timezone Offset: {data.get('timezone', 'N/A')} seconds")
                print(f"Country: {data.get('country', 'N/A')}")
                print(f"Latitude: {data.get('latitude', 'N/A')}")
                print(f"Longitude: {data.get('longitude', 'N/A')}")
                
                current = data.get('current', {})
                print(f"\nCurrent Weather:")
                print(f"  Sunrise: {current.get('sunrise', 'N/A')} (Unix timestamp)")
                print(f"  Sunset: {current.get('sunset', 'N/A')} (Unix timestamp)")
                
                if data.get('daily'):
                    today = data['daily'][0] if data['daily'] else {}
                    print(f"\nDaily Forecast (Today):")
                    print(f"  Sunrise: {today.get('sunrise', 'N/A')} (Unix timestamp)")
                    print(f"  Sunset: {today.get('sunset', 'N/A')} (Unix timestamp)")
            else:
                print(f"\nError for {city}: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"\nException for {city}: {e}")

async def main():
    print("Testing Timezone Data from Backend API")
    print(f"Backend URL: {BASE_URL}")
    
    tasks = [test_city(city) for city in cities]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
