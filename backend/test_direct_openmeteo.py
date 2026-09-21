"""Direct test of Open-Meteo APIs to diagnose 502 connectivity issue."""

import httpx
import asyncio

OPENMETEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPENMETEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def test_geocoding_direct():
    """Test Open-Meteo Geocoding API directly."""
    print("=" * 60)
    print("Testing Open-Meteo Geocoding API Directly")
    print("=" * 60)

    params = {"name": "Bengaluru", "count": 1, "language": "en", "format": "json"}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPENMETEO_GEOCODING_URL, params=params)
            print(f"Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Size: {len(response.content)} bytes")
            
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            if results:
                result = results[0]
                print(f"✓ Found: {result.get('name')}, {result.get('country')}")
                print(f"  Lat: {result.get('latitude')}, Lon: {result.get('longitude')}")
                print(f"  Country Code: {result.get('country_code')}")
                print(f"  Timezone: {result.get('timezone')}")
                return True
            else:
                print("✗ No results found")
                return False
    except httpx.HTTPStatusError as e:
        print(f"✗ HTTP Status Error: {e.response.status_code}")
        print(f"  Response: {e.response.text[:200]}")
        return False
    except httpx.TimeoutException:
        print("✗ Timeout")
        return False
    except httpx.RequestError as e:
        print(f"✗ Request Error: {type(e).__name__}: {e}")
        return False
    except Exception as e:
        print(f"✗ Exception: {type(e).__name__}: {e}")
        return False


async def test_forecast_direct():
    """Test Open-Meteo Forecast API directly."""
    print("\n" + "=" * 60)
    print("Testing Open-Meteo Forecast API Directly")
    print("=" * 60)

    params = {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code,is_day",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,wind_speed_10m_max",
        "timezone": "auto",
        "forecast_days": 7,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPENMETEO_FORECAST_URL, params=params)
            print(f"Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Size: {len(response.content)} bytes")
            
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            daily = data.get("daily", {})
            
            print(f"✓ Current Weather:")
            print(f"  Temperature: {current.get('temperature_2m')}°C")
            print(f"  Weather Code: {current.get('weather_code')}")
            print(f"  Is Day: {current.get('is_day')}")
            
            times = daily.get("time", [])
            print(f"✓ Daily Forecast Days: {len(times)}")
            
            if len(times) > 0:
                print(f"  First day: {times[0]}")
                print(f"  Last day: {times[-1]}")
            
            return True
    except httpx.HTTPStatusError as e:
        print(f"✗ HTTP Status Error: {e.response.status_code}")
        print(f"  Response: {e.response.text[:200]}")
        return False
    except httpx.TimeoutException:
        print("✗ Timeout")
        return False
    except httpx.RequestError as e:
        print(f"✗ Request Error: {type(e).__name__}: {e}")
        return False
    except Exception as e:
        print(f"✗ Exception: {type(e).__name__}: {e}")
        return False


async def main():
    """Run all direct tests."""
    print("\n" + "=" * 60)
    print("DIRECT OPEN-METEO API CONNECTIVITY TEST")
    print("=" * 60)
    
    geocoding_result = await test_geocoding_direct()
    forecast_result = await test_forecast_direct()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Geocoding: {'PASS' if geocoding_result else 'FAIL'}")
    print(f"Forecast: {'PASS' if forecast_result else 'FAIL'}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
