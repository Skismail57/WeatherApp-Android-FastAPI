"""Test WeatherService directly to diagnose 502 issue."""

import asyncio
from app.services.weather_service import WeatherService


async def test_service_direct():
    """Test WeatherService methods directly."""
    print("=" * 60)
    print("Testing WeatherService Directly")
    print("=" * 60)
    
    service = WeatherService()
    
    # Test geocoding
    print("\n1. Testing geocode_city...")
    try:
        geo_data = await service.geocode_city("Bengaluru")
        print(f"✓ Geocoded: {geo_data.get('name')}, {geo_data.get('country')}")
        print(f"  Lat: {geo_data.get('latitude')}, Lon: {geo_data.get('longitude')}")
    except Exception as e:
        print(f"✗ Geocoding failed: {type(e).__name__}: {e}")
        return False
    
    # Test weather by coordinates
    print("\n2. Testing get_weather_by_coordinates...")
    try:
        weather_data = await service.get_weather_by_coordinates(geo_data["latitude"], geo_data["longitude"])
        print(f"✓ Weather fetched: {weather_data.get('temperature')}°C")
        print(f"  Description: {weather_data.get('description')}")
    except Exception as e:
        print(f"✗ Weather fetch failed: {type(e).__name__}: {e}")
        return False
    
    # Test weather by city
    print("\n3. Testing get_weather_by_city...")
    try:
        city_weather = await service.get_weather_by_city("Bengaluru")
        print(f"✓ City weather: {city_weather.get('city')}, {city_weather.get('temperature')}°C")
    except Exception as e:
        print(f"✗ City weather failed: {type(e).__name__}: {e}")
        return False
    
    # Test forecast by coordinates
    print("\n4. Testing get_forecast_by_coordinates...")
    try:
        forecast_data = await service.get_forecast_by_coordinates(geo_data["latitude"], geo_data["longitude"], "Bengaluru", "IN")
        print(f"✓ Forecast fetched: {len(forecast_data.get('daily', []))} days")
        print(f"  Current temp: {forecast_data.get('current', {}).get('temperature')}°C")
    except Exception as e:
        print(f"✗ Forecast fetch failed: {type(e).__name__}: {e}")
        return False
    
    # Test forecast by city
    print("\n5. Testing get_forecast_by_city...")
    try:
        city_forecast = await service.get_forecast_by_city("Bengaluru")
        print(f"✓ City forecast: {city_forecast.get('city')}, {len(city_forecast.get('daily', []))} days")
    except Exception as e:
        print(f"✗ City forecast failed: {type(e).__name__}: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("All service tests passed")
    print("=" * 60)
    return True


if __name__ == "__main__":
    result = asyncio.run(test_service_direct())
    print(f"\nOverall result: {'PASS' if result else 'FAIL'}")
