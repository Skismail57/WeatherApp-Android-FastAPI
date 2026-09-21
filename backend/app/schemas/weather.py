from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    """Normalized current weather response from Open-Meteo API."""

    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    temperature: float = Field(..., description="Temperature in Celsius")
    feels_like: float = Field(..., description="Human-perceived temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
    pressure: float = Field(..., ge=0, description="Atmospheric pressure in hPa")
    wind_speed: float = Field(..., ge=0, description="Wind speed in m/s")
    description: str = Field(..., description="Weather description")
    icon: str = Field(..., description="Weather icon code")
    sunrise: int = Field(default=0, description="Sunrise time as Unix timestamp")
    sunset: int = Field(default=0, description="Sunset time as Unix timestamp")
    timezone: int = Field(default=0, description="Timezone offset in seconds")
    timezone_id: str = Field(default="", description="IANA timezone ID (e.g., Asia/Kolkata)")


class DailyForecast(BaseModel):
    """Daily forecast data from Open-Meteo API."""

    date: int = Field(..., description="Date as Unix timestamp")
    temperature_min: float = Field(..., description="Minimum temperature in Celsius")
    temperature_max: float = Field(..., description="Maximum temperature in Celsius")
    feels_like_day: float = Field(..., description="Daytime feels-like temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
    pressure: float = Field(..., ge=0, description="Atmospheric pressure in hPa")
    wind_speed: float = Field(..., ge=0, description="Wind speed in m/s")
    weather_description: str = Field(..., description="Weather description")
    weather_icon: str = Field(..., description="Weather icon code")
    weather_id: int = Field(
        ..., description="Weather condition ID (WMO code mapped to OpenWeather-like ID)"
    )
    sunrise: int = Field(default=0, description="Sunrise time as Unix timestamp")
    sunset: int = Field(default=0, description="Sunset time as Unix timestamp")


class HourlyForecast(BaseModel):
    """Hourly forecast data from Open-Meteo API."""

    time: int = Field(..., description="Time as Unix timestamp")
    timezone_offset: int = Field(default=0, description="Timezone offset in seconds")
    temperature: float = Field(..., description="Temperature in Celsius")
    weather_code: int = Field(..., description="Weather code (WMO code)")
    weather_description: str = Field(..., description="Weather description")
    weather_icon: str = Field(..., description="Weather icon code")
    precipitation_probability: int = Field(default=0, ge=0, le=100, description="Precipitation probability percentage")
    precipitation: float = Field(default=0, description="Precipitation amount in mm")


class ForecastResponse(BaseModel):
    """Forecast response including current weather, hourly forecast, and daily forecast from Open-Meteo API."""

    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    timezone: int = Field(..., description="Timezone offset in seconds")
    timezone_id: str = Field(default="", description="IANA timezone ID (e.g., Asia/Kolkata)")
    current: WeatherResponse = Field(..., description="Current weather data")
    hourly: list[HourlyForecast] = Field(default_factory=list, description="Hourly forecast list (next 48 hours)")
    daily: list[DailyForecast] = Field(..., description="Daily forecast list (8 days)")


class WeatherAlert(BaseModel):
    """Weather alert/warning from official meteorological sources."""

    id: str = Field(..., description="Alert unique identifier")
    title: str = Field(..., description="Alert title")
    description: str = Field(..., description="Alert description")
    severity: str = Field(..., description="Alert severity (e.g., 'minor', 'moderate', 'severe', 'extreme')")
    area: str = Field(..., description="Affected area")
    effective_time: int = Field(..., description="Effective time as Unix timestamp")
    expires_time: int = Field(..., description="Expiration time as Unix timestamp")
    source: str = Field(..., description="Alert source (e.g., 'IMD', 'NWS')")
    source_url: str = Field(default="", description="URL to official alert details")


class WeatherAlertsResponse(BaseModel):
    """Weather alerts response."""

    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    alerts: list[WeatherAlert] = Field(default_factory=list, description="List of active weather alerts")


class HistoricalWeatherResponse(BaseModel):
    """Historical weather data response from Open-Meteo Historical Weather API."""

    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    timezone: str = Field(..., description="Timezone identifier")
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")
    daily: list[dict] = Field(default_factory=list, description="Daily historical weather data")
