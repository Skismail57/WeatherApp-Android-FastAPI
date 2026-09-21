"""Debug forecast response to diagnose parsing issue."""

import asyncio
import httpx
import json

OPENMETEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def test_forecast_response():
    """Test forecast response structure."""
    print("=" * 60)
    print("Testing Forecast Response Structure")
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
            response.raise_for_status()
            data = response.json()
            
            print("\nFull response structure:")
            print(json.dumps(data, indent=2))
            
            print("\n" + "=" * 60)
            print("Key fields check:")
            print("=" * 60)
            
            print(f"Has 'current': {'current' in data}")
            print(f"Has 'daily': {'daily' in data}")
            print(f"Has 'timezone_offset_seconds': {'timezone_offset_seconds' in data}")
            
            if 'current' in data:
                current = data['current']
                print(f"\nCurrent fields: {list(current.keys())}")
                print(f"Has 'temperature_2m': {'temperature_2m' in current}")
                print(f"Has 'weather_code': {'weather_code' in current}")
                print(f"Has 'is_day': {'is_day' in current}")
            
            if 'daily' in data:
                daily = data['daily']
                print(f"\nDaily fields: {list(daily.keys())}")
                print(f"Has 'time': {'time' in daily}")
                print(f"Has 'weather_code': {'weather_code' in daily}")
                print(f"Has 'temperature_2m_max': {'temperature_2m_max' in daily}")
                print(f"Has 'temperature_2m_min': {'temperature_2m_min' in daily}")
                print(f"Has 'sunrise': {'sunrise' in daily}")
                print(f"Has 'sunset': {'sunset' in daily}")
                
                if 'time' in daily:
                    print(f"\nTime array length: {len(daily['time'])}")
                    print(f"Time values: {daily['time']}")
                
                if 'weather_code' in daily:
                    print(f"\nWeather code array length: {len(daily['weather_code'])}")
                    print(f"Weather code values: {daily['weather_code']}")
                
                if 'sunrise' in daily:
                    print(f"\nSunrise array length: {len(daily['sunrise'])}")
                    print(f"Sunrise values: {daily['sunrise']}")
                
                if 'sunset' in daily:
                    print(f"\nSunset array length: {len(daily['sunset'])}")
                    print(f"Sunset values: {daily['sunset']}")
            
    except Exception as e:
        print(f"✗ Exception: {type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(test_forecast_response())
