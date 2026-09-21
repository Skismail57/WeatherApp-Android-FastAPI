"""
Diagnostic script to identify the root cause of "Weather service unavailable" error.
Run this script to test each component independently.
"""
import asyncio
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_geocoding():
    """Test Open-Meteo geocoding API directly."""
    print("\n=== TEST 1: Open-Meteo Geocoding ===")
    import httpx
    
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": "Bengaluru", "count": 1, "language": "en", "format": "json"}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if results:
                print(f"✅ Geocoding SUCCESS: {results[0]['name']}, {results[0]['country']}")
                print(f"   Coordinates: {results[0]['latitude']}, {results[0]['longitude']}")
                return results[0]
            else:
                print("❌ Geocoding FAILED: No results found")
                return None
    except Exception as e:
        print(f"❌ Geocoding FAILED: {type(e).__name__}: {e}")
        return None

async def test_forecast():
    """Test Open-Meteo forecast API directly."""
    print("\n=== TEST 2: Open-Meteo Forecast ===")
    import httpx
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code,is_day",
        "timezone": "auto",
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            current = data.get("current", {})
            print(f"✅ Forecast SUCCESS")
            print(f"   Temperature: {current.get('temperature_2m')}°C")
            print(f"   Pressure: {current.get('pressure_msl')} hPa")
            print(f"   Humidity: {current.get('relative_humidity_2m')}%")
            return data
    except Exception as e:
        print(f"❌ Forecast FAILED: {type(e).__name__}: {e}")
        return None

async def test_database_connection():
    """Test MySQL database connection."""
    print("\n=== TEST 3: Database Connection ===")
    
    try:
        from app.db.database import SessionLocal, engine
        from sqlalchemy import text
        
        # Test engine connection
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                print("✅ Database engine connection SUCCESS")
        except Exception as e:
            print(f"❌ Database engine connection FAILED: {type(e).__name__}: {e}")
            return False
        
        # Test session
        try:
            db = SessionLocal()
            print("✅ Database session creation SUCCESS")
            db.close()
        except Exception as e:
            print(f"❌ Database session creation FAILED: {type(e).__name__}: {e}")
            return False
        
        return True
    except ImportError as e:
        print(f"❌ Database import FAILED: {type(e).__name__}: {e}")
        print("   Check if DATABASE_URL is set in .env file")
        return False
    except Exception as e:
        print(f"❌ Database test FAILED: {type(e).__name__}: {e}")
        return False

async def test_weather_service():
    """Test WeatherService.get_weather_by_city()."""
    print("\n=== TEST 4: WeatherService.get_weather_by_city() ===")
    
    try:
        from app.services.weather_service import WeatherService
        
        service = WeatherService()
        result = await service.get_weather_by_city("Bengaluru")
        print(f"✅ WeatherService SUCCESS")
        print(f"   City: {result.get('city')}")
        print(f"   Temperature: {result.get('temperature')}°C")
        print(f"   Pressure: {result.get('pressure')} hPa")
        return result
    except Exception as e:
        print(f"❌ WeatherService FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_weather_service_geocode():
    """Test WeatherService.geocode_city() only."""
    print("\n=== TEST 5: WeatherService.geocode_city() ===")
    
    try:
        from app.services.weather_service import WeatherService
        
        service = WeatherService()
        result = await service.geocode_city("Bengaluru")
        print(f"✅ Geocode SUCCESS")
        print(f"   Name: {result.get('name')}")
        print(f"   Country: {result.get('country')}")
        print(f"   Coordinates: {result.get('latitude')}, {result.get('longitude')}")
        return result
    except Exception as e:
        print(f"❌ Geocode FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_weather_service_coordinates():
    """Test WeatherService.get_weather_by_coordinates() only."""
    print("\n=== TEST 6: WeatherService.get_weather_by_coordinates() ===")
    
    try:
        from app.services.weather_service import WeatherService
        
        service = WeatherService()
        result = await service.get_weather_by_coordinates(12.9716, 77.5946)
        print(f"✅ Coordinates weather SUCCESS")
        print(f"   Temperature: {result.get('temperature')}°C")
        print(f"   Pressure: {result.get('pressure')} hPa")
        return result
    except Exception as e:
        print(f"❌ Coordinates weather FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    """Run all diagnostic tests."""
    print("=" * 60)
    print("WEATHER SERVICE DIAGNOSTIC")
    print("=" * 60)
    
    # Test 1: Direct Open-Meteo Geocoding
    geo_result = await test_geocoding()
    
    # Test 2: Direct Open-Meteo Forecast
    forecast_result = await test_forecast()
    
    # Test 3: Database Connection
    db_ok = await test_database_connection()
    
    # Test 4: WeatherService.geocode_city()
    service_geo_result = await test_weather_service_geocode()
    
    # Test 5: WeatherService.get_weather_by_coordinates()
    service_coords_result = await test_weather_service_coordinates()
    
    # Test 6: WeatherService.get_weather_by_city()
    service_result = await test_weather_service()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Open-Meteo Geocoding: {'✅ PASS' if geo_result else '❌ FAIL'}")
    print(f"Open-Meteo Forecast: {'✅ PASS' if forecast_result else '❌ FAIL'}")
    print(f"Database Connection: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"WeatherService.geocode_city: {'✅ PASS' if service_geo_result else '❌ FAIL'}")
    print(f"WeatherService.get_weather_by_coordinates: {'✅ PASS' if service_coords_result else '❌ FAIL'}")
    print(f"WeatherService.get_weather_by_city: {'✅ PASS' if service_result else '❌ FAIL'}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
