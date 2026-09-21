from sqlalchemy import desc

from app.db.database import SessionLocal
from app.db.models.forecast import WeatherForecast
from app.db.models.weather import WeatherRecord

db = SessionLocal()
try:
    # Check weather_records table
    records = db.query(WeatherRecord).order_by(desc(WeatherRecord.created_at)).limit(10).all()
    print(f"Found {len(records)} recent weather records:")
    for record in records:
        print(
            f"  - {record.city}, {record.country}: {record.temperature}°C, {record.weather_description} (created: {record.created_at})"
        )

    # Check weather_forecasts table
    forecasts = db.query(WeatherForecast).order_by(desc(WeatherForecast.created_at)).limit(10).all()
    print(f"\nFound {len(forecasts)} recent forecast records:")
    for forecast in forecasts:
        print(
            f"  - {forecast.city}, {forecast.country}: {forecast.temperature_min}°C-{forecast.temperature_max}°C, "
            f"{forecast.weather_description} (forecast_date: {forecast.forecast_date}, created: {forecast.created_at})"
        )
finally:
    db.close()
