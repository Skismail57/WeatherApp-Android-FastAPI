# Weather Platform API

## Overview

This FastAPI backend provides a shared API for the Weather Android and Web applications. It serves as a centralized weather data service, normalizing responses from the Open-Meteo API and providing a consistent interface for both mobile and web clients.

## Technology Stack

- **Python 3.11+**
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation using Python type annotations
- **Pydantic Settings** - Settings management using environment variables
- **SQLAlchemy 2.x** - SQL toolkit and ORM
- **MySQL** - Relational database
- **httpx** - Async HTTP client for external API calls
- **Open-Meteo API** - Free weather data provider (geocoding and forecast)
- **PyMySQL** - MySQL driver for Python
- **pytest** - Testing framework
- **pytest-asyncio** - Async support for pytest
- **Ruff** - Fast Python linter
- **Black** - Python code formatter

## Project Structure

```
backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── health.py       # Health check endpoint
│   │       └── weather.py      # Weather API endpoints
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Application configuration
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py         # Database session management
│   │   ├── init_db.py          # Database initialization
│   │   └── models/
│   │       ├── __init__.py
│   │       ├── forecast.py     # Forecast data model
│   │       └── weather.py      # Weather data model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py           # Common response schemas
│   │   └── weather.py          # Weather response schemas
│   │
│   └── services/
│       ├── __init__.py
│       └── weather_service.py  # Weather business logic
│
├── tests/
│   ├── __init__.py
│   ├── test_health.py          # Health endpoint tests
│   └── test_weather.py         # Weather endpoint tests
│
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## Configuration

1. Copy the example environment file:
   ```powershell
   cp .env.example .env
   ```

2. Edit `.env` and add your configuration:
   ```env
   APP_NAME=Weather Platform API
   APP_VERSION=1.0.0
   DEBUG=true

   DATABASE_URL=mysql+pymysql://weather_user:password@localhost:3306/weather_db

   CORS_ORIGINS=http://localhost:5173
   ```

**Important:** Never commit `.env` to version control. It contains sensitive information.

## Run Locally

1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

5. Start the development server:
   ```powershell
   uvicorn app.main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

### Root Endpoint
- **GET /** - Returns API status message

### Health Endpoint
- **GET /api/v1/health** - Health check endpoint

### Weather Endpoints

#### Get Weather by City
- **Endpoint**: `GET /api/v1/weather/city/{city}`
- **Description**: Fetch current weather data for a specific city using Open-Meteo API
- **Parameters**:
  - `city` (path): City name (case-insensitive, max 100 characters)
- **Response**: Normalized weather data including temperature, humidity, wind, etc.
- **Example**:
  ```bash
  curl http://localhost:8000/api/v1/weather/city/Bengaluru
  ```

#### Get Weather by Coordinates
- **Endpoint**: `GET /api/v1/weather/coordinates`
- **Description**: Fetch current weather data by coordinates using Open-Meteo API
- **Parameters**:
  - `lat` (query): Latitude (-90 to 90)
  - `lon` (query): Longitude (-180 to 180)
- **Response**: Normalized weather data
- **Example**:
  ```bash
  curl "http://localhost:8000/api/v1/weather/coordinates?lat=12.9716&lon=77.5946"
  ```

#### Get Forecast by City
- **Endpoint**: `GET /api/v1/weather/city/{city}/forecast`
- **Description**: Fetch weather forecast for a specific city using Open-Meteo API
- **Parameters**:
  - `city` (path): City name (case-insensitive, max 100 characters)
- **Response**: Current weather and 6-day forecast
- **Example**:
  ```bash
  curl http://localhost:8000/api/v1/weather/city/Bengaluru/forecast
  ```

#### Get Forecast by Coordinates
- **Endpoint**: `GET /api/v1/weather/coordinates/forecast`
- **Description**: Fetch weather forecast by coordinates using Open-Meteo API
- **Parameters**:
  - `lat` (query): Latitude (-90 to 90)
  - `lon` (query): Longitude (-180 to 180)
- **Response**: Current weather and 6-day forecast
- **Example**:
  ```bash
  curl "http://localhost:8000/api/v1/weather/coordinates/forecast?lat=12.9716&lon=77.5946"
  ```

### Error Responses

- **400 Bad Request**: Invalid input parameters
- **404 Not Found**: City not found
- **422 Unprocessable Entity**: Invalid coordinates
- **502 Bad Gateway**: Weather service unavailable
- **503 Service Unavailable**: Weather service timeout
- **500 Internal Server Error**: Unexpected server error

## Testing

Run the test suite:
```powershell
pytest
```

Run tests with coverage:
```powershell
pytest --cov=app
```

## Database

The application uses MySQL with SQLAlchemy ORM. The database connection is configured via the `DATABASE_URL` environment variable.

### MySQL Setup

1. Ensure MySQL Server 8.0+ is installed and running
2. Create the database:
   ```sql
   CREATE DATABASE weather_db;
   ```
3. Create a dedicated user (recommended):
   ```sql
   CREATE USER 'weather_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON weather_db.* TO 'weather_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Database Initialization

The application automatically initializes the database schema on startup using SQLAlchemy metadata creation. The following tables will be created automatically when the server starts:

- **weather_records** - Stores current weather data
- **weather_forecasts** - Stores daily forecast data

To manually initialize the database:
```powershell
python -c "from app.db.init_db import init_db; init_db()"
```

## Security

- No API keys required (Open-Meteo is free and doesn't require authentication)
- Database credentials are loaded from environment variables
- `.env` is excluded from version control
- CORS is configured to allow specific origins only
- Sensitive information is never logged
- Error responses do not expose internal details
- All OpenWeather API keys and references have been removed

## Development

### Code Formatting
```powershell
black app/ tests/
```

### Linting
```powershell
ruff check app/ tests/
```

### Auto-format with Ruff
```powershell
ruff format app/ tests/
```

## Architecture

The backend follows a layered architecture:

```
┌─────────────────────┐
│   Android Weather   │
│     Native Java     │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│      FastAPI        │
│     /api/v1         │
└───────┬───────┬─────┘
        │       │
        │       │
        ▼       ▼
┌───────────┐ ┌───────────────┐
│ Open-Meteo │ │     MySQL     │
│  Provider  │ │   Database    │
└───────────┘ └───────────────┘

           ▲
           │ HTTP
┌──────────┴──────────┐
│    React Web App    │
│      Later          │
└─────────────────────┘
```

## License

See the project root LICENSE file.
