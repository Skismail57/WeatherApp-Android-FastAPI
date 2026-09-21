"""Test database save operations to isolate the issue."""

import asyncio
from app.services.weather_service import WeatherService


async def test_database_save():
    """Test database save operations."""
    print("=" * 60)
    print("Testing Database Save Operations")
    print("=" * 60)
    
    service = WeatherService()
    
    # Test geocoding
    print("\n1. Testing geocode_city...")
    try:
        geo_data = await service.geocode_city("Bengaluru")
        print(f"✓ Geocoded: {geo_data.get('name')}")
    except Exception as e:
        print(f"✗ Geocoding failed: {type(e).__name__}: {e}")
        return False
    
    # Test weather by coordinates (this should trigger DB save)
    print("\n2. Testing get_weather_by_coordinates (with DB save)...")
    try:
        weather_data = await service.get_weather_by_coordinates(geo_data["latitude"], geo_data["longitude"])
        print(f"✓ Weather fetched: {weather_data.get('temperature')}°C")
        print("  Database save attempted")
    except Exception as e:
        print(f"✗ Weather fetch failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test forecast by coordinates (this should trigger DB save)
    print("\n3. Testing get_forecast_by_coordinates (with DB save)...")
    try:
        forecast_data = await service.get_forecast_by_coordinates(geo_data["latitude"], geo_data["longitude"], "Bengaluru", "IN")
        print(f"✓ Forecast fetched: {len(forecast_data.get('daily', []))} days")
        print("  Database save attempted")
    except Exception as e:
        print(f"✗ Forecast fetch failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("Database save tests completed")
    print("=" * 60)
    return True


if __name__ == "__main__":
    result = asyncio.run(test_database_save())
    print(f"\nOverall result: {'PASS' if result else 'FAIL'}")
