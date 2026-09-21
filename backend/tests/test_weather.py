from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.services.weather_service.httpx.AsyncClient")
def test_weather_endpoint_success(mock_client):
    """Test weather endpoint success with Open-Meteo mocking."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.return_value = {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "name": "Bengaluru",
            "country": "India",
            "country_code": "IN",
            "timezone": "Asia/Kolkata",
        }

        with patch(
            "app.services.weather_service.WeatherService.get_weather_by_coordinates",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = {
                "city": "Bengaluru",
                "country": "IN",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "temperature": 24.5,
                "feels_like": 25.1,
                "humidity": 72,
                "pressure": 1012,
                "wind_speed": 3.2,
                "description": "Clear sky",
                "icon": "01d",
                "sunrise": 0,
                "sunset": 0,
                "timezone": 19800,
            }

            response = client.get("/api/v1/weather/city/Bengaluru")
            assert response.status_code == 200
            data = response.json()
            assert data["city"] == "Bengaluru"
            assert data["country"] == "IN"
            assert data["temperature"] == 24.5


def test_weather_endpoint_not_found():
    """Test weather endpoint with city not found."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.side_effect = ValueError("City not found")

        response = client.get("/api/v1/weather/city/InvalidCity")
        assert response.status_code == 404


def test_weather_endpoint_timeout():
    """Test weather endpoint with timeout."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.side_effect = ValueError("Geocoding service timeout")

        response = client.get("/api/v1/weather/city/Bengaluru")
        assert response.status_code == 503


def test_weather_endpoint_server_failure():
    """Test weather endpoint with server failure."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.side_effect = ValueError("Geocoding service unavailable")

        response = client.get("/api/v1/weather/city/Bengaluru")
        assert response.status_code == 502


def test_weather_endpoint_invalid_city():
    """Test weather endpoint with invalid city."""
    response = client.get("/api/v1/weather/city/   ")
    assert response.status_code == 400


def test_weather_endpoint_empty_city():
    """Test weather endpoint with empty city."""
    response = client.get("/api/v1/weather/city/")
    assert response.status_code == 404  # FastAPI will return 404 for empty path


def test_weather_endpoint_malformed_response():
    """Test weather endpoint with malformed response."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.return_value = {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "name": "Bengaluru",
            "country": "India",
            "country_code": "IN",
            "timezone": "Asia/Kolkata",
        }

        with patch(
            "app.services.weather_service.WeatherService.get_weather_by_coordinates",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.side_effect = ValueError("Invalid weather data format")

            response = client.get("/api/v1/weather/city/Bengaluru")
            assert response.status_code == 502


def test_weather_endpoint_no_secrets_in_response():
    """Ensure API responses do not contain secrets."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.return_value = {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "name": "Bengaluru",
            "country": "India",
            "country_code": "IN",
            "timezone": "Asia/Kolkata",
        }

        with patch(
            "app.services.weather_service.WeatherService.get_weather_by_coordinates",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = {
                "city": "Bengaluru",
                "country": "IN",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "temperature": 24.5,
                "feels_like": 25.1,
                "humidity": 72,
                "pressure": 1012,
                "wind_speed": 3.2,
                "description": "Clear sky",
                "icon": "01d",
                "sunrise": 0,
                "sunset": 0,
                "timezone": 19800,
            }

            response = client.get("/api/v1/weather/city/Bengaluru")
            assert response.status_code == 200
            data = response.json()
            response_str = str(data).lower()

            # Check for common secret indicators
            assert "api_key" not in response_str
            assert "password" not in response_str
            assert "mysql+pymysql" not in response_str
            assert "1802b8f42bcc85edeb13ada3fd7cc2ff" not in response_str
            assert "weather123" not in response_str


def test_weather_coordinates_success():
    """Test weather by coordinates endpoint."""
    with patch(
        "app.services.weather_service.WeatherService.get_weather_by_coordinates",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = {
            "city": "Bengaluru",
            "country": "IN",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "temperature": 24.5,
            "feels_like": 25.1,
            "humidity": 72,
            "pressure": 1012,
            "wind_speed": 3.2,
            "description": "Clear sky",
            "icon": "01d",
            "sunrise": 1694768400,
            "sunset": 1694811600,
            "timezone": 19800,
        }

        response = client.get("/api/v1/weather/coordinates?lat=12.9716&lon=77.5946")
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Bengaluru"
        assert data["latitude"] == 12.9716
        assert data["longitude"] == 77.5946


def test_weather_coordinates_invalid_latitude():
    """Test invalid latitude validation."""
    response = client.get("/api/v1/weather/coordinates?lat=91&lon=77.5946")
    assert response.status_code == 422  # FastAPI validation error


def test_weather_coordinates_invalid_longitude():
    """Test invalid longitude validation."""
    response = client.get("/api/v1/weather/coordinates?lat=12.9716&lon=181")
    assert response.status_code == 422  # FastAPI validation error


def test_forecast_city_success():
    """Test forecast by city endpoint."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.return_value = {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "name": "Bengaluru",
            "country": "India",
            "country_code": "IN",
            "timezone": "Asia/Kolkata",
        }

        with patch(
            "app.services.weather_service.WeatherService.get_forecast_by_coordinates",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = {
                "city": "Bengaluru",
                "country": "IN",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "timezone": 19800,
                "current": {
                    "city": "Bengaluru",
                    "country": "IN",
                    "latitude": 12.9716,
                    "longitude": 77.5946,
                    "temperature": 24.5,
                    "feels_like": 25.1,
                    "humidity": 72,
                    "pressure": 1012,
                    "wind_speed": 3.2,
                    "description": "Clear sky",
                    "icon": "01d",
                    "sunrise": 1694768400,
                    "sunset": 1694811600,
                    "timezone": 19800,
                },
                "daily": [
                    {
                        "date": 1694854800,
                        "temperature_min": 20.0,
                        "temperature_max": 28.0,
                        "feels_like_day": 26.0,
                        "humidity": 70,
                        "pressure": 1010,
                        "wind_speed": 3.0,
                        "weather_description": "Clear sky",
                        "weather_icon": "01d",
                        "weather_id": 800,
                        "sunrise": 1694768400,
                        "sunset": 1694811600,
                    }
                ],
            }

            response = client.get("/api/v1/weather/city/Bengaluru/forecast")
            assert response.status_code == 200
            data = response.json()
            assert data["city"] == "Bengaluru"
            assert "current" in data
            assert "daily" in data
            assert len(data["daily"]) > 0


def test_forecast_city_not_found():
    """Test forecast with city not found."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.side_effect = ValueError("City not found")

        response = client.get("/api/v1/weather/city/InvalidCity/forecast")
        assert response.status_code == 404


def test_forecast_coordinates_success():
    """Test forecast by coordinates endpoint."""
    with patch(
        "app.services.weather_service.WeatherService.get_forecast_by_coordinates",
        new_callable=AsyncMock,
    ) as mock_get:
        mock_get.return_value = {
            "city": "Bengaluru",
            "country": "IN",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "timezone": 19800,
            "current": {
                "city": "Bengaluru",
                "country": "IN",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "temperature": 24.5,
                "feels_like": 25.1,
                "humidity": 72,
                "pressure": 1012,
                "wind_speed": 3.2,
                "description": "Clear sky",
                "icon": "01d",
                "sunrise": 1694768400,
                "sunset": 1694811600,
                "timezone": 19800,
            },
            "daily": [
                {
                    "date": 1694854800,
                    "temperature_min": 20.0,
                    "temperature_max": 28.0,
                    "feels_like_day": 26.0,
                    "humidity": 70,
                    "pressure": 1010,
                    "wind_speed": 3.0,
                    "weather_description": "Clear sky",
                    "weather_icon": "01d",
                    "weather_id": 800,
                    "sunrise": 1694768400,
                    "sunset": 1694811600,
                }
            ],
        }

        response = client.get("/api/v1/weather/coordinates/forecast?lat=12.9716&lon=77.5946")
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Bengaluru"
        assert "current" in data
        assert "daily" in data


def test_forecast_coordinates_invalid():
    """Test forecast with invalid coordinates."""
    response = client.get("/api/v1/weather/coordinates/forecast?lat=91&lon=77.5946")
    assert response.status_code == 422  # FastAPI validation error


def test_worldwide_city_london():
    """Test worldwide city - London."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.return_value = {
            "latitude": 51.5074,
            "longitude": -0.1278,
            "name": "London",
            "country": "United Kingdom",
            "country_code": "GB",
            "timezone": "Europe/London",
        }

        with patch(
            "app.services.weather_service.WeatherService.get_weather_by_coordinates",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = {
                "city": "London",
                "country": "GB",
                "latitude": 51.5074,
                "longitude": -0.1278,
                "temperature": 15.5,
                "feels_like": 14.8,
                "humidity": 80,
                "pressure": 1015,
                "wind_speed": 4.5,
                "description": "Light rain",
                "icon": "10d",
                "sunrise": 0,
                "sunset": 0,
                "timezone": 3600,
            }

            response = client.get("/api/v1/weather/city/London")
            assert response.status_code == 200
            data = response.json()
            assert data["city"] == "London"
            assert data["country"] == "GB"


def test_worldwide_city_new_york():
    """Test worldwide city - New York."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.return_value = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "name": "New York",
            "country": "United States",
            "country_code": "US",
            "timezone": "America/New_York",
        }

        with patch(
            "app.services.weather_service.WeatherService.get_weather_by_coordinates",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = {
                "city": "New York",
                "country": "US",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "temperature": 18.0,
                "feels_like": 17.5,
                "humidity": 65,
                "pressure": 1018,
                "wind_speed": 5.2,
                "description": "Clear sky",
                "icon": "01d",
                "sunrise": 0,
                "sunset": 0,
                "timezone": -14400,
            }

            response = client.get("/api/v1/weather/city/New%20York")
            assert response.status_code == 200
            data = response.json()
            assert data["city"] == "New York"
            assert data["country"] == "US"


def test_worldwide_city_tokyo():
    """Test worldwide city - Tokyo."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.return_value = {
            "latitude": 35.6762,
            "longitude": 139.6503,
            "name": "Tokyo",
            "country": "Japan",
            "country_code": "JP",
            "timezone": "Asia/Tokyo",
        }

        with patch(
            "app.services.weather_service.WeatherService.get_weather_by_coordinates",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = {
                "city": "Tokyo",
                "country": "JP",
                "latitude": 35.6762,
                "longitude": 139.6503,
                "temperature": 22.0,
                "feels_like": 22.5,
                "humidity": 75,
                "pressure": 1010,
                "wind_speed": 3.8,
                "description": "Overcast",
                "icon": "04d",
                "sunrise": 0,
                "sunset": 0,
                "timezone": 32400,
            }

            response = client.get("/api/v1/weather/city/Tokyo")
            assert response.status_code == 200
            data = response.json()
            assert data["city"] == "Tokyo"
            assert data["country"] == "JP"


def test_forecast_no_secrets():
    """Ensure forecast responses do not contain secrets."""
    with patch(
        "app.services.weather_service.WeatherService.geocode_city", new_callable=AsyncMock
    ) as mock_geocode:
        mock_geocode.return_value = {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "name": "Bengaluru",
            "country": "India",
            "country_code": "IN",
            "timezone": "Asia/Kolkata",
        }

        with patch(
            "app.services.weather_service.WeatherService.get_forecast_by_coordinates",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = {
                "city": "Bengaluru",
                "country": "IN",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "timezone": 19800,
                "current": {
                    "city": "Bengaluru",
                    "country": "IN",
                    "latitude": 12.9716,
                    "longitude": 77.5946,
                    "temperature": 24.5,
                    "feels_like": 25.1,
                    "humidity": 72,
                    "pressure": 1012,
                    "wind_speed": 3.2,
                    "description": "Clear sky",
                    "icon": "01d",
                    "sunrise": 1694768400,
                    "sunset": 1694811600,
                    "timezone": 19800,
                },
                "daily": [],
            }

            response = client.get("/api/v1/weather/city/Bengaluru/forecast")
            assert response.status_code == 200
            data = response.json()
            response_str = str(data).lower()

            assert "api_key" not in response_str
            assert "password" not in response_str
            assert "mysql+pymysql" not in response_str
