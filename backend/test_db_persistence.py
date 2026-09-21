"""
Test MySQL persistence of weather records.
"""
from app.db.database import SessionLocal
from app.db.models.weather import WeatherRecord
from app.db.models.forecast import WeatherForecast

def test_weather_records():
    """Check if weather records are being saved."""
    print("=== Testing Weather Records ===")
    
    db = SessionLocal()
    try:
        records = db.query(WeatherRecord).order_by(WeatherRecord.created_at.desc()).limit(5).all()
        
        if records:
            print(f"✅ Found {len(records)} recent weather records:")
            for record in records:
                print(f"  - {record.city}, {record.country}: {record.temperature}°C, Pressure: {record.pressure} hPa")
        else:
            print("❌ No weather records found in database")
    except Exception as e:
        print(f"❌ Error querying weather records: {type(e).__name__}: {e}")
    finally:
        db.close()

def test_forecast_records():
    """Check if forecast records are being saved."""
    print("\n=== Testing Forecast Records ===")
    
    db = SessionLocal()
    try:
        records = db.query(WeatherForecast).order_by(WeatherForecast.created_at.desc()).limit(10).all()
        
        if records:
            print(f"✅ Found {len(records)} recent forecast records:")
            for record in records:
                print(f"  - {record.city}: {record.temperature_min}°C to {record.temperature_max}°C, Pressure: {record.pressure} hPa")
        else:
            print("❌ No forecast records found in database")
    except Exception as e:
        print(f"❌ Error querying forecast records: {type(e).__name__}: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_weather_records()
    test_forecast_records()
