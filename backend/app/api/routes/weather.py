import logging

from fastapi import APIRouter, HTTPException, Query

from app.schemas.weather import ForecastResponse, WeatherResponse, WeatherAlertsResponse, HistoricalWeatherResponse
from app.services.weather_service import WeatherService

logger = logging.getLogger(__name__)

router = APIRouter()

# NOTE: Production deployment should add rate limiting to prevent abuse
# Consider using slowapi or similar middleware for rate limiting
# Example: from slowapi import Limiter; limiter = Limiter(key_func=get_remote_address)


@router.get("/city/{city}", response_model=WeatherResponse, summary="Get weather by city name")
async def get_weather_by_city(city: str):
    """
    Fetch current weather data for a specific city using Open-Meteo API.

    - **city**: Name of the city (case-insensitive, max 100 characters)
    - **Returns**: Normalized weather data including temperature, humidity, wind, etc.
    - **404**: City not found
    - **502**: Weather service unavailable
    - **503**: Weather service timeout
    - **500**: Internal server error
    """
    weather_service = WeatherService()
    try:
        logger.info(f"Weather request for city: {city}")
        weather_data = await weather_service.get_weather_by_city(city)
        logger.info(f"Weather data received: {weather_data}")
        response = WeatherResponse(**weather_data)
        logger.info("Response created successfully")
        return response
    except HTTPException:
        raise
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Weather service error for {city}: {error_msg}")
        if "city not found" in error_msg.lower():
            raise HTTPException(status_code=404, detail="City not found")
        if "timeout" in error_msg.lower():
            raise HTTPException(status_code=503, detail="Weather service timeout")
        if "empty" in error_msg.lower() or "too long" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Invalid city name")
        raise HTTPException(status_code=502, detail="Weather service unavailable")
    except Exception:
        logger.exception(f"Unexpected error fetching weather for {city}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/coordinates", response_model=WeatherResponse, summary="Get weather by coordinates")
async def get_weather_by_coordinates(
    lat: float = Query(..., ge=-90, le=90, description="Latitude in decimal degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in decimal degrees"),
):
    """
    Fetch current weather data by coordinates using Open-Meteo API.

    - **lat**: Latitude (-90 to 90)
    - **lon**: Longitude (-180 to 180)
    - **Returns**: Normalized weather data including temperature, humidity, wind, etc.
    - **400**: Invalid coordinates
    - **502**: Weather service unavailable
    - **503**: Weather service timeout
    - **500**: Internal server error
    """
    weather_service = WeatherService()
    try:
        logger.info(f"Weather request for coordinates: {lat}, {lon}")
        weather_data = await weather_service.get_weather_by_coordinates(lat, lon)
        return WeatherResponse(**weather_data)
    except HTTPException:
        raise
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Weather service error for coordinates: {error_msg}")
        if "timeout" in error_msg.lower():
            raise HTTPException(status_code=503, detail="Weather service timeout")
        if "invalid latitude" in error_msg.lower() or "invalid longitude" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Invalid coordinates")
        raise HTTPException(status_code=502, detail="Weather service unavailable")
    except Exception:
        logger.exception("Unexpected error fetching weather for coordinates")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/city/{city}/forecast", response_model=ForecastResponse, summary="Get forecast by city name"
)
async def get_forecast_by_city(city: str):
    """
    Fetch weather forecast for a specific city using Open-Meteo API.

    - **city**: Name of the city (case-insensitive, max 100 characters)
    - **Returns**: Current weather and 6-day forecast
    - **404**: City not found
    - **502**: Weather service unavailable
    - **503**: Weather service timeout
    - **500**: Internal server error
    """
    weather_service = WeatherService()
    try:
        logger.info(f"Forecast request for city: {city}")
        forecast_data = await weather_service.get_forecast_by_city(city)
        return ForecastResponse(**forecast_data)
    except HTTPException:
        raise
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Weather service error for forecast {city}: {error_msg}")
        if "city not found" in error_msg.lower():
            raise HTTPException(status_code=404, detail="City not found")
        if "timeout" in error_msg.lower():
            raise HTTPException(status_code=503, detail="Weather service timeout")
        if "empty" in error_msg.lower() or "too long" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Invalid city name")
        raise HTTPException(status_code=502, detail="Weather service unavailable")
    except Exception:
        logger.exception(f"Unexpected error fetching forecast for {city}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/coordinates/forecast", response_model=ForecastResponse, summary="Get forecast by coordinates"
)
async def get_forecast_by_coordinates(
    lat: float = Query(..., ge=-90, le=90, description="Latitude in decimal degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in decimal degrees"),
):
    """
    Fetch weather forecast by coordinates using Open-Meteo API.

    - **lat**: Latitude (-90 to 90)
    - **lon**: Longitude (-180 to 180)
    - **Returns**: Current weather, 48-hour hourly forecast, and 8-day daily forecast
    - **400**: Invalid coordinates
    - **502**: Weather service unavailable
    - **503**: Weather service timeout
    - **500**: Internal server error
    """
    weather_service = WeatherService()
    try:
        logger.info(f"Forecast request for coordinates: {lat}, {lon}")
        forecast_data = await weather_service.get_forecast_by_coordinates(lat, lon)
        return ForecastResponse(**forecast_data)
    except HTTPException:
        raise
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Weather service error for forecast coordinates: {error_msg}")
        if "timeout" in error_msg.lower():
            raise HTTPException(status_code=503, detail="Weather service timeout")
        if "invalid latitude" in error_msg.lower() or "invalid longitude" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Invalid coordinates")
        raise HTTPException(status_code=502, detail="Weather service unavailable")
    except Exception:
        logger.exception("Unexpected error fetching forecast for coordinates")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/coordinates/alerts", response_model=WeatherAlertsResponse, summary="Get weather alerts by coordinates"
)
async def get_weather_alerts_by_coordinates(
    lat: float = Query(..., ge=-90, le=90, description="Latitude in decimal degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in decimal degrees"),
):
    """
    Fetch weather alerts for a location.

    NOTE: An official weather alert provider is NOT currently configured.
    This endpoint returns an empty alerts list. To enable real weather alerts,
    integrate with an official meteorological service (e.g., NWS, Met Office, IMD).

    - **lat**: Latitude (-90 to 90)
    - **lon**: Longitude (-180 to 180)
    - **Returns**: List of active weather alerts (currently always empty)
    - **400**: Invalid coordinates
    - **500**: Internal server error
    """
    weather_service = WeatherService()
    try:
        logger.info(f"Weather alerts request for coordinates: {lat}, {lon}")
        alerts_data = await weather_service.get_weather_alerts(lat, lon)
        return WeatherAlertsResponse(**alerts_data)
    except HTTPException:
        raise
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Weather alerts error for coordinates: {error_msg}")
        if "invalid latitude" in error_msg.lower() or "invalid longitude" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Invalid coordinates")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception:
        logger.exception("Unexpected error fetching weather alerts")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/coordinates/historical", response_model=HistoricalWeatherResponse, summary="Get historical weather by coordinates"
)
async def get_historical_weather_by_coordinates(
    lat: float = Query(..., ge=-90, le=90, description="Latitude in decimal degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in decimal degrees"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format (minimum 1979-01-01)"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format (maximum today)"),
):
    """
    Fetch historical weather data from Open-Meteo Historical Weather API.

    - **lat**: Latitude (-90 to 90)
    - **lon**: Longitude (-180 to 180)
    - **start_date**: Start date in YYYY-MM-DD format (minimum 1979-01-01)
    - **end_date**: End date in YYYY-MM-DD format (maximum today)
    - **Returns**: Historical weather data for the specified date range
    - **400**: Invalid coordinates or date range
    - **502**: Weather service unavailable
    - **503**: Weather service timeout
    - **500**: Internal server error
    """
    weather_service = WeatherService()
    try:
        logger.info(f"Historical weather request for coordinates: {lat}, {lon}, dates: {start_date} to {end_date}")
        historical_data = await weather_service.get_historical_weather(lat, lon, start_date, end_date)
        return HistoricalWeatherResponse(**historical_data)
    except HTTPException:
        raise
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Historical weather error: {error_msg}")
        if "invalid latitude" in error_msg.lower() or "invalid longitude" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Invalid coordinates")
        if "date" in error_msg.lower():
            raise HTTPException(status_code=400, detail=error_msg)
        raise HTTPException(status_code=502, detail="Weather service unavailable")
    except Exception:
        logger.exception("Unexpected error fetching historical weather")
        raise HTTPException(status_code=500, detail="Internal server error")
