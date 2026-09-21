"""
Test Pydantic schema validation directly.
"""
import asyncio
from app.services.weather_service import WeatherService
from app.schemas.weather import WeatherResponse

async def test_schema_validation():
    """Test if WeatherService output matches WeatherResponse schema."""
    print("=== Testing Schema Validation ===")
    
    service = WeatherService()
    weather_data = await service.get_weather_by_city("Bengaluru")
    
    print("\nWeatherService returned:")
    for key, value in weather_data.items():
        print(f"  {key}: {value} ({type(value).__name__})")
    
    print("\n=== Attempting to create WeatherResponse ===")
    try:
        response = WeatherResponse(**weather_data)
        print("✅ Schema validation SUCCESS")
        print(f"  City: {response.city}")
        print(f"  Temperature: {response.temperature}")
        print(f"  Pressure: {response.pressure}")
        return response
    except Exception as e:
        print(f"❌ Schema validation FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_schema_validation())
