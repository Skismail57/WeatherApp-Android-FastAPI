from sqlalchemy import Column, DateTime, Float, Index, Integer, String
from sqlalchemy.sql import func

from app.db.database import Base


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    country = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    forecast_date = Column(Integer, index=True)  # Unix timestamp
    temperature_min = Column(Float)
    temperature_max = Column(Float)
    feels_like_day = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Float)  # Changed from Integer to Float to match Open-Meteo
    wind_speed = Column(Float)
    weather_description = Column(String(100))
    weather_icon = Column(String(10))
    weather_id = Column(Integer)
    sunrise = Column(Integer)
    sunset = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Add composite indexes for common queries
    __table_args__ = (
        Index("idx_city_forecast_date", "city", "forecast_date"),
        Index("idx_coordinates", "latitude", "longitude"),
    )
