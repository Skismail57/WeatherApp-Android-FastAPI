from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.db.database import Base


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    country = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Float)  # Changed from Integer to Float to match Open-Meteo
    wind_speed = Column(Float)
    weather_description = Column(String(100))
    weather_icon = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
