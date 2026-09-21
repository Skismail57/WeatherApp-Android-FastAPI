import logging
from datetime import datetime, timezone, timedelta

import httpx

from app.db.database import SessionLocal
from app.db.models.forecast import WeatherForecast
from app.db.models.weather import WeatherRecord
from app.utils.weather_codes import (
    weather_code_to_condition_id,
    weather_code_to_description,
    weather_code_to_icon,
)

logger = logging.getLogger(__name__)

# Open-Meteo API endpoints
OPENMETEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPENMETEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPENMETEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"


class WeatherService:
    def __init__(self):
        self.geocoding_url = OPENMETEO_GEOCODING_URL
        self.forecast_url = OPENMETEO_FORECAST_URL
        self.historical_url = OPENMETEO_HISTORICAL_URL

    def _validate_city(self, city: str) -> str:
        """Validate and normalize city name."""
        if not city or not city.strip():
            raise ValueError("City name cannot be empty")
        city = city.strip()
        if len(city) > 100:
            raise ValueError("City name too long")
        return city

    def _validate_coordinates(self, lat: float, lon: float) -> tuple[float, float]:
        """Validate latitude and longitude."""
        if not (-90 <= lat <= 90):
            raise ValueError("Invalid latitude: must be between -90 and 90")
        if not (-180 <= lon <= 180):
            raise ValueError("Invalid longitude: must be between -180 and 180")
        return lat, lon

    async def geocode_city(self, city: str) -> dict:
        """Geocode city name to coordinates using Open-Meteo Geocoding API.

        Args:
            city: City name

        Returns:
            Dictionary with latitude, longitude, name, country, country_code, timezone

        Raises:
            ValueError: If city not found or API error
        """
        city = self._validate_city(city)

        params = {"name": city, "count": 1, "language": "en", "format": "json"}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.geocoding_url, params=params)
                response.raise_for_status()
                data = response.json()

                results = data.get("results", [])
                if not results:
                    logger.warning(f"City not found: {city}")
                    raise ValueError("City not found")

                result = results[0]
                logger.info(f"Successfully geocoded city: {city}")
                return {
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                    "name": result.get("name"),
                    "country": result.get("country"),
                    "country_code": result.get("country_code"),
                    "timezone": result.get("timezone"),
                }
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error geocoding {city}: {e.response.status_code}")
            raise ValueError("Geocoding service unavailable")
        except httpx.TimeoutException:
            logger.error(f"Timeout geocoding {city}")
            raise ValueError("Geocoding service timeout")
        except httpx.RequestError as e:
            logger.error(f"Request error geocoding {city}: {type(e).__name__}")
            raise ValueError("Geocoding service unavailable")
        except ValueError:
            logger.error(f"Invalid response from geocoding API for {city}")
            raise ValueError("Geocoding service returned invalid data")

    async def get_weather_by_coordinates(self, lat: float, lon: float) -> dict:
        """Fetch current weather data by coordinates from Open-Meteo Forecast API.

        Args:
            lat: Latitude (-90 to 90)
            lon: Longitude (-180 to 180)

        Returns:
            Normalized weather data dictionary
        """
        lat, lon = self._validate_coordinates(lat, lon)

        # Request current weather data from Open-Meteo
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code,is_day",
            "timezone": "auto",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.forecast_url, params=params)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Successfully fetched weather for coordinates: {lat}, {lon}")
                normalized = self._normalize_current_response(data, lat, lon)
                self._save_weather_record(normalized)
                return normalized
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching weather for coordinates: {e.response.status_code}")
            raise ValueError("Weather service unavailable")
        except httpx.TimeoutException:
            logger.error("Timeout fetching weather for coordinates")
            raise ValueError("Weather service timeout")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching weather for coordinates: {type(e).__name__}")
            raise ValueError("Weather service unavailable")
        except ValueError:
            logger.error("Invalid response from weather API for coordinates")
            raise ValueError("Weather service returned invalid data")

    async def get_weather_by_city(self, city: str) -> dict:
        """Fetch weather data by city name.

        Args:
            city: City name

        Returns:
            Normalized weather data dictionary
        """
        city = self._validate_city(city)

        # Geocode city to get coordinates
        geo_data = await self.geocode_city(city)

        # Get weather using coordinates
        weather_data = await self.get_weather_by_coordinates(
            geo_data["latitude"], geo_data["longitude"]
        )

        # Add city/country info from geocoding
        weather_data["city"] = geo_data["name"]
        weather_data["country"] = geo_data["country_code"]

        return weather_data

    async def get_forecast_by_coordinates(
        self, lat: float, lon: float, city: str = "Unknown", country: str = ""
    ) -> dict:
        """Fetch forecast data by coordinates from Open-Meteo Forecast API.

        Args:
            lat: Latitude (-90 to 90)
            lon: Longitude (-180 to 180)
            city: City name (optional, for response)
            country: Country code (optional, for response)

        Returns:
            Normalized forecast data dictionary with current weather, hourly forecast, and daily forecast
        """
        lat, lon = self._validate_coordinates(lat, lon)

        # Request current weather, hourly forecast, and daily forecast from Open-Meteo
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code,is_day",
            "hourly": "temperature_2m,weather_code,precipitation_probability,precipitation",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,wind_speed_10m_max,uv_index_max",
            "timezone": "auto",
            "forecast_days": 9,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.forecast_url, params=params)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Successfully fetched forecast for coordinates: {lat}, {lon}")
                normalized = self._normalize_forecast_response(data, city, country, lat, lon)
                self._save_forecast_records(normalized)
                return normalized
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching forecast for coordinates: {e.response.status_code}")
            raise ValueError("Weather service unavailable")
        except httpx.TimeoutException:
            logger.error("Timeout fetching forecast for coordinates")
            raise ValueError("Weather service timeout")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching forecast for coordinates: {type(e).__name__}")
            raise ValueError("Weather service unavailable")
        except ValueError:
            logger.error("Invalid response from weather API for forecast")
            raise ValueError("Weather service returned invalid data")

    async def get_forecast_by_city(self, city: str) -> dict:
        """Fetch forecast data by city name.

        Args:
            city: City name

        Returns:
            Normalized forecast data dictionary
        """
        city = self._validate_city(city)

        # Geocode city to get coordinates
        geo_data = await self.geocode_city(city)

        # Get forecast using coordinates
        forecast_data = await self.get_forecast_by_coordinates(
            geo_data["latitude"], geo_data["longitude"], geo_data["name"], geo_data["country_code"]
        )

        return forecast_data

    def _normalize_current_response(self, data: dict, lat: float, lon: float) -> dict:
        """Normalize Open-Meteo current weather response to internal format.

        Args:
            data: Open-Meteo API response
            lat: Latitude
            lon: Longitude

        Returns:
            Normalized weather data dictionary
        """
        try:
            current = data.get("current", {})
            weather_code = current.get("weather_code", 0)
            is_day = current.get("is_day", 1)

            return {
                "city": "Unknown",  # Will be filled by caller if using city endpoint
                "country": "",  # Will be filled by caller if using city endpoint
                "latitude": lat,
                "longitude": lon,
                "temperature": current.get("temperature_2m"),
                "feels_like": current.get("apparent_temperature"),
                "humidity": current.get("relative_humidity_2m"),
                "pressure": current.get("pressure_msl"),
                "wind_speed": current.get("wind_speed_10m"),
                "description": weather_code_to_description(weather_code),
                "icon": weather_code_to_icon(weather_code, is_day == 1),
                "sunrise": 0,  # Not available in current endpoint, will be in forecast
                "sunset": 0,  # Not available in current endpoint, will be in forecast
                "timezone": data.get("utc_offset_seconds", 0),  # Open-Meteo uses utc_offset_seconds
                "timezone_id": data.get("timezone", ""),  # IANA timezone ID (e.g., Asia/Kolkata)
            }
            logger.info(f"DEBUG - Current Weather Normalized - City: Unknown, timezone_id: {data.get('timezone', '')}, utc_offset_seconds: {data.get('utc_offset_seconds', 0)}, sunrise: 0, sunset: 0")
        except (KeyError, IndexError, AttributeError) as e:
            logger.error(f"Failed to normalize current weather response: {e}")
            raise ValueError("Invalid weather data format")

    def _normalize_forecast_response(
        self, data: dict, city: str, country: str, lat: float, lon: float
    ) -> dict:
        """Normalize Open-Meteo forecast response to internal format.

        Args:
            data: Open-Meteo API response
            city: City name
            country: Country code
            lat: Latitude
            lon: Longitude

        Returns:
            Normalized forecast data dictionary
        """
        try:
            current = data.get("current", {})
            daily = data.get("daily", {})
            weather_code = current.get("weather_code", 0)
            is_day = current.get("is_day", 1)

            # Helper function to convert ISO8601 string to Unix timestamp
            def iso_to_unix(iso_string: str, offset_seconds: int = 0) -> int:
                """Convert ISO8601 string to Unix timestamp.
                
                Open-Meteo returns naive ISO strings in the location's timezone when timezone=auto is used.
                We need to apply the location's timezone offset before converting to Unix timestamp.
                """
                try:
                    dt = datetime.fromisoformat(iso_string)
                    # Open-Meteo naive datetimes are in location timezone, apply offset to get UTC
                    if dt.tzinfo is None and offset_seconds != 0:
                        dt = dt.replace(tzinfo=timezone.utc) - timedelta(seconds=offset_seconds)
                    elif dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return int(dt.timestamp())
                except (ValueError, AttributeError):
                    return 0

            # Normalize current weather
            normalized_current = {
                "city": city,
                "country": country,
                "latitude": lat,
                "longitude": lon,
                "temperature": current.get("temperature_2m"),
                "feels_like": current.get("apparent_temperature"),
                "humidity": current.get("relative_humidity_2m"),
                "pressure": current.get("pressure_msl"),
                "wind_speed": current.get("wind_speed_10m"),
                "description": weather_code_to_description(weather_code),
                "icon": weather_code_to_icon(weather_code, is_day == 1),
                "sunrise": (
                    iso_to_unix(daily.get("sunrise", [""])[0]) if daily.get("sunrise") else 0
                ),
                "sunset": iso_to_unix(daily.get("sunset", [""])[0]) if daily.get("sunset") else 0,
                "timezone": data.get("utc_offset_seconds", 0),  # Open-Meteo uses utc_offset_seconds
                "timezone_id": data.get("timezone", ""),  # IANA timezone ID (e.g., Asia/Kolkata)
            }

            # Get timezone offset for use in hourly forecasts
            utc_offset = data.get("utc_offset_seconds", 0)

            # Normalize daily forecast (include today and next 6 days for total 7-day forecast)
            daily_forecast = []
            times = daily.get("time", [])
            weather_codes = daily.get("weather_code", [])
            temp_max = daily.get("temperature_2m_max", [])
            temp_min = daily.get("temperature_2m_min", [])
            feels_like_max = daily.get("apparent_temperature_max", [])
            sunrise = daily.get("sunrise", [])
            sunset = daily.get("sunset", [])
            wind_max = daily.get("wind_speed_10m_max", [])
            uv_index_max = daily.get("uv_index_max", [])

            # Include today and next 6 days for a total 7-day forecast
            for i in range(0, min(7, len(times))):
                day_code = weather_codes[i] if i < len(weather_codes) else 0
                day_data = {
                    "date": iso_to_unix(times[i]) if i < len(times) else 0,
                    "temperature_min": temp_min[i] if i < len(temp_min) else 0,
                    "temperature_max": temp_max[i] if i < len(temp_max) else 0,
                    "feels_like_day": feels_like_max[i] if i < len(feels_like_max) else 0,
                    "humidity": normalized_current["humidity"],  # Use current humidity
                    "pressure": normalized_current["pressure"],  # Use current pressure
                    "wind_speed": wind_max[i] if i < len(wind_max) else 0,
                    "weather_description": weather_code_to_description(day_code),
                    "weather_icon": weather_code_to_icon(day_code, True),
                    "weather_id": weather_code_to_condition_id(day_code),
                    "sunrise": iso_to_unix(sunrise[i]) if i < len(sunrise) else 0,
                    "sunset": iso_to_unix(sunset[i]) if i < len(sunset) else 0,
                }
                daily_forecast.append(day_data)

            # Normalize hourly forecast (next 48 hours)
            hourly_forecast = []
            hourly_data = data.get("hourly", {})
            hourly_times = hourly_data.get("time", [])
            hourly_temps = hourly_data.get("temperature_2m", [])
            hourly_codes = hourly_data.get("weather_code", [])
            hourly_precip = hourly_data.get("precipitation_probability", [])
            hourly_precip_amount = hourly_data.get("precipitation", [])

            # Get current hour index by finding the hourly record closest to current time
            current_hour_index = 0

            # Use current weather time to find the appropriate hourly index
            current_time = current.get("time", "")
            if current_time:
                # Current time is in ISO format, find matching hourly index
                for i, iso_time in enumerate(hourly_times):
                    if iso_time.startswith(current_time[:13]):  # Match up to hour
                        current_hour_index = i
                        break

            logger.info(f"Current time: {current_time}, Starting hourly from index: {current_hour_index}, ISO time: {hourly_times[current_hour_index] if current_hour_index < len(hourly_times) else 'N/A'}")

            # Get next 48 hours from current hour
            for i in range(current_hour_index, min(current_hour_index + 48, len(hourly_times))):
                hour_code = hourly_codes[i] if i < len(hourly_codes) else 0
                iso_time = hourly_times[i] if i < len(hourly_times) else ""
                unix_time = iso_to_unix(iso_time, utc_offset)
                logger.info(f"Hourly[{i}] - ISO: {iso_time}, Open-Meteo timezone: {data.get('timezone', 'auto')}, utc_offset_seconds: {utc_offset}, Unix: {unix_time}")
                hour_data = {
                    "time": unix_time,
                    "timezone_offset": utc_offset,
                    "temperature": hourly_temps[i] if i < len(hourly_temps) else 0,
                    "weather_code": hour_code,
                    "weather_description": weather_code_to_description(hour_code),
                    "weather_icon": weather_code_to_icon(hour_code, True),
                    "precipitation_probability": hourly_precip[i] if i < len(hourly_precip) else 0,
                    "precipitation": hourly_precip_amount[i] if i < len(hourly_precip_amount) else 0,
                }
                hourly_forecast.append(hour_data)

            return {
                "city": city,
                "country": country,
                "latitude": lat,
                "longitude": lon,
                "timezone": data.get("utc_offset_seconds", 0),  # Open-Meteo uses utc_offset_seconds
                "timezone_id": data.get("timezone", ""),  # IANA timezone ID (e.g., Asia/Kolkata)
                "current": normalized_current,
                "hourly": hourly_forecast,
                "daily": daily_forecast,
            }
            logger.info(f"DEBUG - Forecast Normalized - City: {city}, timezone_id: {data.get('timezone', '')}, utc_offset_seconds: {data.get('utc_offset_seconds', 0)}, current_sunrise: {normalized_current.get('sunrise', 0)}, current_sunset: {normalized_current.get('sunset', 0)}")
        except (KeyError, IndexError, AttributeError) as e:
            logger.error(f"Failed to normalize forecast response: {e}")
            raise ValueError("Invalid forecast data format")

    def _save_weather_record(self, weather_data: dict):
        """Save weather record to database."""
        try:
            db = SessionLocal()
            record = WeatherRecord(
                city=weather_data.get("city"),
                country=weather_data.get("country"),
                latitude=weather_data.get("latitude"),
                longitude=weather_data.get("longitude"),
                temperature=weather_data.get("temperature"),
                feels_like=weather_data.get("feels_like"),
                humidity=weather_data.get("humidity"),
                pressure=weather_data.get("pressure"),
                wind_speed=weather_data.get("wind_speed"),
                weather_description=weather_data.get("description"),
                weather_icon=weather_data.get("icon"),
            )
            db.add(record)
            db.commit()
            logger.info(f"Saved weather record for city: {weather_data.get('city')}")
        except Exception:
            logger.exception("Failed to save weather record")
            # Don't raise - allow the request to succeed even if DB save fails
        finally:
            db.close()

    def _save_forecast_records(self, forecast_data: dict):
        """Save forecast records to database."""
        try:
            db = SessionLocal()
            city = forecast_data.get("city")
            country = forecast_data.get("country")
            latitude = forecast_data.get("latitude")
            longitude = forecast_data.get("longitude")

            for day in forecast_data.get("daily", []):
                record = WeatherForecast(
                    city=city,
                    country=country,
                    latitude=latitude,
                    longitude=longitude,
                    forecast_date=day.get("date"),
                    temperature_min=day.get("temperature_min"),
                    temperature_max=day.get("temperature_max"),
                    feels_like_day=day.get("feels_like_day"),
                    humidity=day.get("humidity"),
                    pressure=day.get("pressure"),
                    wind_speed=day.get("wind_speed"),
                    weather_description=day.get("weather_description"),
                    weather_icon=day.get("weather_icon"),
                    weather_id=day.get("weather_id"),
                    sunrise=day.get("sunrise"),
                    sunset=day.get("sunset"),
                )
                db.add(record)
            db.commit()
            logger.info(f"Saved forecast records for city: {city}")
        except Exception:
            logger.exception("Failed to save forecast records")
            # Don't raise - allow the request to succeed even if DB save fails
        finally:
            db.close()

    async def get_historical_weather(
        self, lat: float, lon: float, start_date: str, end_date: str
    ) -> dict:
        """Fetch historical weather data from Open-Meteo Historical Weather API.

        Args:
            lat: Latitude (-90 to 90)
            lon: Longitude (-180 to 180)
            start_date: Start date in YYYY-MM-DD format (minimum 1979-01-01)
            end_date: End date in YYYY-MM-DD format (maximum today)

        Returns:
            Normalized historical weather data dictionary
        """
        lat, lon = self._validate_coordinates(lat, lon)

        # Validate date range
        min_date = datetime(1979, 1, 1).date()
        max_date = datetime.now().date()

        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        if start_dt < min_date:
            raise ValueError(f"Start date must be {min_date} or later")
        if end_dt > max_date:
            raise ValueError("End date cannot be in the future")
        if start_dt > end_dt:
            raise ValueError("Start date must be before or equal to end date")

        # Limit date range to prevent excessive requests (max 1 year)
        date_diff = (end_dt - start_dt).days
        if date_diff > 365:
            raise ValueError("Date range cannot exceed 1 year")

        # Request historical weather data from Open-Meteo
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,precipitation_hours,wind_speed_10m_max,relative_humidity_2m_mean",
            "timezone": "auto",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.historical_url, params=params)
                response.raise_for_status()
                data = response.json()
                logger.info(f"Successfully fetched historical weather for coordinates: {lat}, {lon}")
                return self._normalize_historical_response(data, lat, lon, start_date, end_date)
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching historical weather: {e.response.status_code}")
            raise ValueError("Weather service unavailable")
        except httpx.TimeoutException:
            logger.error("Timeout fetching historical weather")
            raise ValueError("Weather service timeout")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching historical weather: {type(e).__name__}")
            raise ValueError("Weather service unavailable")
        except ValueError:
            logger.error("Invalid response from historical weather API")
            raise ValueError("Weather service returned invalid data")

    def _normalize_historical_response(
        self, data: dict, lat: float, lon: float, start_date: str, end_date: str
    ) -> dict:
        """Normalize Open-Meteo historical weather response to internal format.

        Args:
            data: Open-Meteo Historical API response
            lat: Latitude
            lon: Longitude
            start_date: Start date string
            end_date: End date string

        Returns:
            Normalized historical weather data dictionary
        """
        try:
            daily = data.get("daily", {})
            times = daily.get("time", [])

            daily_data = []
            for i, time_str in enumerate(times):
                daily_record = {
                    "date": time_str,
                    "temperature_max": daily.get("temperature_2m_max", [])[i] if i < len(daily.get("temperature_2m_max", [])) else None,
                    "temperature_min": daily.get("temperature_2m_min", [])[i] if i < len(daily.get("temperature_2m_min", [])) else None,
                    "temperature_mean": daily.get("temperature_2m_mean", [])[i] if i < len(daily.get("temperature_2m_mean", [])) else None,
                    "precipitation_sum": daily.get("precipitation_sum", [])[i] if i < len(daily.get("precipitation_sum", [])) else 0,
                    "precipitation_hours": daily.get("precipitation_hours", [])[i] if i < len(daily.get("precipitation_hours", [])) else 0,
                    "wind_speed_max": daily.get("wind_speed_10m_max", [])[i] if i < len(daily.get("wind_speed_10m_max", [])) else 0,
                    "humidity_mean": daily.get("relative_humidity_2m_mean", [])[i] if i < len(daily.get("relative_humidity_2m_mean", [])) else 0,
                }
                daily_data.append(daily_record)

            return {
                "latitude": lat,
                "longitude": lon,
                "timezone": data.get("timezone", "UTC"),
                "start_date": start_date,
                "end_date": end_date,
                "daily": daily_data,
            }
        except (KeyError, IndexError, AttributeError) as e:
            logger.error(f"Failed to normalize historical weather response: {e}")
            raise ValueError("Invalid historical weather data format")

    async def get_weather_alerts(
        self, lat: float, lon: float, city: str = "Unknown", country: str = ""
    ) -> dict:
        """Fetch weather alerts for a location.

        NOTE: An official weather alert provider is NOT currently configured.
        This endpoint returns an empty alerts list. To enable real weather alerts,
        integrate with an official meteorological service (e.g., NWS, Met Office, IMD).

        Args:
            lat: Latitude (-90 to 90)
            lon: Longitude (-180 to 180)
            city: City name (optional, for response)
            country: Country code (optional, for response)

        Returns:
            Weather alerts response with list of alerts (currently always empty)
        """
        lat, lon = self._validate_coordinates(lat, lon)

        # No official alert source configured - return empty list
        # Future: Integrate with official meteorological service for real alerts
        logger.info(f"Weather alerts requested for {city} ({lat}, {lon}) - no official alert source configured")

        return {
            "city": city,
            "country": country,
            "latitude": lat,
            "longitude": lon,
            "alerts": [],
        }
