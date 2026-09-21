"""Manual verification script for Open-Meteo APIs.

This script tests real Open-Meteo API calls to verify:
1. Geocoding API works correctly
2. Forecast API works correctly
3. WMO code mapping functions work correctly
"""

import asyncio
import httpx

from app.utils.weather_codes import (
    weather_code_to_condition_id,
    weather_code_to_description,
    weather_code_to_icon,
)

OPENMETEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPENMETEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


async def test_geocoding():
    """Test Open-Meteo Geocoding API."""
    print("=" * 60)
    print("Testing Open-Meteo Geocoding API")
    print("=" * 60)

    cities = ["Bengaluru", "London", "New York", "Tokyo", "Paris"]

    for city in cities:
        print(f"\nGeocoding: {city}")
        params = {"name": city, "count": 1, "language": "en", "format": "json"}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(OPENMETEO_GEOCODING_URL, params=params)
                response.raise_for_status()
                data = response.json()

                results = data.get("results", [])
                if results:
                    result = results[0]
                    print(f"  ✓ Found: {result.get('name')}, {result.get('country')}")
                    print(f"    Lat: {result.get('latitude')}, Lon: {result.get('longitude')}")
                    print(f"    Country Code: {result.get('country_code')}")
                else:
                    print(f"  ✗ Not found")
        except Exception as e:
            print(f"  ✗ Error: {e}")


async def test_forecast():
    """Test Open-Meteo Forecast API."""
    print("\n" + "=" * 60)
    print("Testing Open-Meteo Forecast API")
    print("=" * 60)

    # Test with known coordinates (Bengaluru)
    lat, lon = 12.9716, 77.5946
    print(f"\nFetching forecast for: {lat}, {lon}")

    params = {
        "latitude": lat,
        "longitude": lon,
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

            current = data.get("current", {})
            daily = data.get("daily", {})

            print(f"  ✓ Current Weather:")
            print(f"    Temperature: {current.get('temperature_2m')}°C")
            print(f"    Feels Like: {current.get('apparent_temperature')}°C")
            print(f"    Humidity: {current.get('relative_humidity_2m')}%")
            print(f"    Pressure: {current.get('pressure_msl')} hPa")
            print(f"    Wind Speed: {current.get('wind_speed_10m')} m/s")
            print(f"    Weather Code: {current.get('weather_code')}")
            print(f"    Is Day: {current.get('is_day')}")

            times = daily.get("time", [])
            weather_codes = daily.get("weather_code", [])
            temp_max = daily.get("temperature_2m_max", [])
            temp_min = daily.get("temperature_2m_min", [])

            print(f"\n  ✓ Daily Forecast (next 6 days):")
            for i in range(1, min(7, len(times))):
                print(f"    Day {i}: {times[i]}")
                print(f"      Temp: {temp_min[i]}°C - {temp_max[i]}°C")
                print(f"      Weather Code: {weather_codes[i]}")

    except Exception as e:
        print(f"  ✗ Error: {e}")


def test_wmo_mapping():
    """Test WMO weather code mapping functions."""
    print("\n" + "=" * 60)
    print("Testing WMO Weather Code Mapping")
    print("=" * 60)

    test_codes = [0, 1, 2, 3, 45, 61, 63, 65, 71, 73, 75, 95, 96, 99]

    for code in test_codes:
        description = weather_code_to_description(code)
        icon_day = weather_code_to_icon(code, is_day=True)
        icon_night = weather_code_to_icon(code, is_day=False)
        condition_id = weather_code_to_condition_id(code)

        print(f"\n  Code {code}:")
        print(f"    Description: {description}")
        print(f"    Icon (Day): {icon_day}")
        print(f"    Icon (Night): {icon_night}")
        print(f"    Condition ID: {condition_id}")


async def main():
    """Run all verification tests."""
    print("\n" + "=" * 60)
    print("OPEN-METEO API VERIFICATION")
    print("=" * 60)

    await test_geocoding()
    await test_forecast()
    test_wmo_mapping()

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
