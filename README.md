# Weather App - Android + FastAPI

![Cover Image](App%20Screenshots/github%20cover%20image.png)

A comprehensive cross-platform weather application featuring a native Android frontend and FastAPI backend, powered by free Open-Meteo APIs for accurate weather data.

## 📱 App Demo Video

<img src="App%20Screenshots/APP%20WORKING%20VIDEO.gif" width="250">

## 📸 App Screenshots

<table>
  <tr>
    <td><img src="App%20Screenshots/Screenshot_20260921-111503_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-111558_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-111624_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-111642_Weather%20Forecast.jpg" width="250"></td>
  </tr>
  <tr>
    <td><img src="App%20Screenshots/Screenshot_20260921-111731_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-111900_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-111944_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112014_Weather%20Forecast.jpg" width="250"></td>
  </tr>
  <tr>
    <td><img src="App%20Screenshots/Screenshot_20260921-112036_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112100_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112121_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112141_Weather%20Forecast.jpg" width="250"></td>
  </tr>
  <tr>
    <td><img src="App%20Screenshots/Screenshot_20260921-112203_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112226_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112248_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112311_Weather%20Forecast.jpg" width="250"></td>
  </tr>
  <tr>
    <td><img src="App%20Screenshots/Screenshot_20260921-112331_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112504_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112529_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112544_Weather%20Forecast.jpg" width="250"></td>
  </tr>
  <tr>
    <td><img src="App%20Screenshots/Screenshot_20260921-112606_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112618_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112625_Weather%20Forecast.jpg" width="250"></td>
    <td><img src="App%20Screenshots/Screenshot_20260921-112631_Weather%20Forecast.jpg" width="250"></td>
  </tr>
</table>

## ✨ Features

### Android App Features
- **Current Weather**: Real-time weather data with temperature, humidity, pressure, wind speed
- **48-Hour Hourly Forecast**: Detailed hourly weather predictions for the next 48 hours
- **7-Day Daily Forecast**: Extended weather forecast for the next 7 days
- **GPS Location Detection**: Automatic location detection using device GPS
- **City Search**: Search for weather in any city worldwide using voice or text input
- **Historical Weather**: Access historical weather data from 1979 onwards
- **Beautiful UI**: Material Design with smooth animations using Lottie
- **Swipe to Refresh**: Pull-to-refresh functionality for instant weather updates
- **Auto-Update Support**: In-app update mechanism for seamless app updates
- **Responsive Design**: Adaptive UI that works on different screen sizes
- **Offline Support**: Shows cached data when offline
- **Timezone Support**: Automatic timezone detection and display
- **Sunrise/Sunset Times**: Accurate sunrise and sunset information

### Backend API Features
- **RESTful API**: Clean and well-documented FastAPI endpoints
- **Open-Meteo Integration**: Free weather data without API keys
- **Geocoding Support**: City name to coordinates conversion
- **Current Weather**: Real-time weather data endpoint
- **Forecast API**: Comprehensive forecast with hourly and daily data
- **Historical Weather**: Historical weather data from 1979
- **Weather Alerts**: Architecture for weather warning integration
- **Database Persistence**: MySQL database for weather history
- **Input Validation**: Robust validation using Pydantic schemas
- **Error Handling**: Comprehensive error handling and logging
- **CORS Support**: Configurable CORS for cross-origin requests
- **Security Headers**: Built-in security middleware

## 🏗️ Architecture

```
Android App (Java)
    ↓ HTTP Requests
FastAPI REST API (Python)
    ↓ HTTP Requests
Open-Meteo APIs (Free Weather Data)
    ↓
MySQL Database (Persistence)
```

### Components

- **Android App**: Native Android application built with Java, featuring Material Design UI
- **FastAPI Backend**: Python REST API serving weather data with async support
- **Open-Meteo**: Free weather forecast and geocoding API (no API key required)
- **MySQL**: Relational database for weather history and forecast caching

## 🛠️ Technology Stack

### Android Frontend

#### Core Technologies
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="40" height="40"> **Language**: Java
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/gradle/gradle-plain.svg" width="40" height="40"> **Build System**: Gradle 8.13
- **Android Gradle Plugin**: 8.13.2
- **Compile SDK**: 36
- **Target SDK**: 36
- **Minimum SDK**: 19 (Android 4.4+)
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/openjdk/openjdk-original.svg" width="40" height="40"> **JDK**: 17

#### Libraries & Dependencies
- **Networking**: Volley 1.2.1 - HTTP client for API requests
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" width="40" height="40"> **Location Services**: Google Play Services Location 21.0.1 - GPS and location detection
- **UI Components**:
  - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/materialdesign/materialdesign-original.svg" width="40" height="40"> Material Design Components 1.9.0
  - AppCompat 1.6.1
  - ConstraintLayout 2.1.4
  - SwipeRefreshLayout 1.1.0
- **Animations**:
  - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/lottie/lottie-original.svg" width="40" height="40"> Lottie 5.2.0 - High-quality animations
  - SpinKit 1.4.0 - Loading indicators
- **Custom Components**:
  - Roasted Toast 1.0.2 - Custom toast messages
  - SDP Android 1.1.0 - Responsive screen size scaling
- **App Updates**: Google Play Core 1.10.3 - In-app update functionality
- **MultiDex**: MultiDex 2.0.1 - Support for large applications

### Backend API

#### Core Technologies
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40"> **Language**: Python 3.11+
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="40" height="40"> **Framework**: FastAPI 0.115.0 - Modern, fast web framework
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/uvicorn/uvicorn-original.svg" width="40" height="40"> **ASGI Server**: Uvicorn 0.32.0 - Lightning-fast ASGI server
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/httpx/httpx-original.svg" width="40" height="40"> **HTTP Client**: httpx 0.27.2 - Async HTTP client
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original.svg" width="40" height="40"> **ORM**: SQLAlchemy 2.0.35 - SQL toolkit and ORM
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" width="40" height="40"> **Database Driver**: PyMySQL 1.1.1 - MySQL connector
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pydantic/pydantic-original.svg" width="40" height="40"> **Validation**: Pydantic 2.9.2 - Data validation using Python type annotations
- **Settings**: Pydantic Settings 2.6.0 - Configuration management
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dotenv/dotenv-original.svg" width="40" height="40"> **Environment**: python-dotenv 1.0.1 - Environment variable management

#### Testing
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytest/pytest-original.svg" width="40" height="40"> **pytest**: 8.3.3 - Testing framework
- **pytest-asyncio**: 0.24.0 - Async testing support

### External APIs

- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/openmeteo/openmeteo-original.svg" width="40" height="40"> **Open-Meteo Geocoding API**: `https://geocoding-api.open-meteo.com/v1/search`
  - Converts city names to coordinates
  - Free, no API key required
  - Supports worldwide locations
  
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/openmeteo/openmeteo-original.svg" width="40" height="40"> **Open-Meteo Forecast API**: `https://api.open-meteo.com/v1/forecast`
  - Current weather data
  - Hourly forecasts (up to 48 hours)
  - Daily forecasts (up to 7 days)
  - Historical weather data (from 1979)
  - Free for non-commercial use

- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/openmeteo/openmeteo-original.svg" width="40" height="40"> **Open-Meteo Historical API**: `https://archive-api.open-meteo.com/v1/archive`
  - Historical weather data
  - Data available from 1979-01-01
  - Maximum 1-year range per request

### Database

- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" width="40" height="40"> **MySQL 8.0+**: Relational database for persistence
- **Tables**:
  - `weather_records` - Current weather data
  - `weather_forecasts` - Forecast data

## 📁 Project Structure

```
WeatherApp-Android-master/
├── app/                                    # Android application
│   ├── src/main/
│   │   ├── java/com/Ismail/weatherapp/
│   │   │   ├── HomeActivity.java           # Main weather screen
│   │   │   ├── SplashScreen.java           # Splash screen with animation
│   │   │   ├── HistoricalWeatherActivity.java # Historical weather screen
│   │   │   ├── adapter/
│   │   │   │   ├── DaysAdapter.java        # Daily forecast adapter
│   │   │   │   ├── HourlyAdapter.java      # Hourly forecast adapter
│   │   │   │   └── HistoricalAdapter.java  # Historical data adapter
│   │   │   ├── model/
│   │   │   │   ├── DailyWeather.java       # Daily forecast model
│   │   │   │   ├── HourlyWeather.java      # Hourly forecast model
│   │   │   │   ├── HistoricalWeatherData.java # Historical data model
│   │   │   │   └── WeatherAlert.java       # Weather alert model
│   │   │   ├── network/
│   │   │   │   ├── WeatherApiClient.java   # FastAPI client
│   │   │   │   └── InternetConnectivity.java # Network checker
│   │   │   ├── location/
│   │   │   │   ├── LocationCord.java       # Coordinate storage
│   │   │   │   └── CityFinder.java        # Geocoding utility
│   │   │   ├── update/
│   │   │   │   └── UpdateUI.java           # UI update helpers
│   │   │   ├── toast/
│   │   │   │   └── Toaster.java            # Custom toast messages
│   │   │   ├── url/
│   │   │   │   └── URL.java                # URL constants
│   │   │   └── utils/
│   │   │       └── TimeUtils.java          # Time formatting utilities
│   │   ├── res/                            # Android resources
│   │   │   ├── layout/                     # XML layouts
│   │   │   ├── drawable/                   # Drawables and icons
│   │   │   ├── values/                     # Strings, colors, styles
│   │   │   └── raw/                        # Raw files (Lottie animations)
│   │   └── AndroidManifest.xml            # App manifest
│   └── build.gradle                        # App-level Gradle config
├── backend/                                # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py               # Health check endpoint
│   │   │       └── weather.py              # Weather endpoints
│   │   ├── core/
│   │   │   └── config.py                   # Configuration settings
│   │   ├── db/
│   │   │   ├── database.py                 # Database connection
│   │   │   ├── init_db.py                  # Database initialization
│   │   │   └── models/
│   │   │       ├── weather.py              # Weather record model
│   │   │       └── forecast.py             # Forecast record model
│   │   ├── schemas/
│   │   │   └── weather.py                  # Pydantic schemas
│   │   ├── services/
│   │   │   └── weather_service.py          # Business logic
│   │   ├── utils/
│   │   │   └── weather_codes.py            # WMO code mapping
│   │   └── main.py                         # FastAPI application entry
│   ├── tests/
│   │   ├── test_health.py                  # Health endpoint tests
│   │   └── test_weather.py                 # Weather endpoint tests
│   ├── requirements.txt                    # Python dependencies
│   ├── .env.example                        # Environment variables template
│   ├── .env                                # Environment variables (not in git)
│   └── README.md                           # Backend documentation
├── App Screenshots/                        # App screenshots and demo video
├── local.properties                        # Local configuration (not in git)
├── build.gradle                            # Root Gradle file
├── gradle.properties                       # Gradle properties
├── settings.gradle                         # Gradle settings
├── gradlew                                 # Gradle wrapper (Unix)
├── gradlew.bat                             # Gradle wrapper (Windows)
└── README.md                               # This file
```

## 🚀 Installation & Setup

### Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.11+** - For backend development
- **MySQL 8.0+** - Database server
- **Android Studio** - For Android development
- **JDK 17** - Java Development Kit
- **Git** - Version control
- **ADB** - Android Debug Bridge (included with Android Studio)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   
   On Windows:
   ```bash
   .venv\Scripts\activate
   ```
   
   On Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your database credentials:
   ```env
   APP_NAME=Weather Platform API
   APP_VERSION=1.0.0
   DEBUG=true
   
   DATABASE_URL=mysql+pymysql://weather_user:password@localhost:3306/weather_db
   
   CORS_ORIGINS_STR=http://localhost:5173
   ```

6. **Create MySQL database**
   ```sql
   CREATE DATABASE weather_db;
   CREATE USER 'weather_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON weather_db.* TO 'weather_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

7. **Initialize database tables**
   ```bash
   python -c "from app.db.init_db import init_db; init_db()"
   ```

8. **Start FastAPI server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

9. **Verify backend is running**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2024-09-21T06:30:00.000000Z"
   }
   ```

### Android Setup

1. **Open project in Android Studio**
   - Launch Android Studio
   - Select "Open an Existing Project"
   - Navigate to the project root directory
   - Click "OK"

2. **Configure backend URL**
   
   Create or edit `local.properties` in the project root directory:
   
   For **Android Emulator**:
   ```properties
   BACKEND_BASE_URL=http://10.0.2.2:8000
   ```
   
   For **Physical Android Device**:
   ```properties
   BACKEND_BASE_URL=http://127.0.0.1:8000
   ```
   
   Then run the following command to forward the backend port:
   ```bash
   adb reverse tcp:8000 tcp:8000
   ```

3. **Sync Gradle files**
   - Android Studio will automatically prompt to sync Gradle
   - Click "Sync Now" when prompted
   - Wait for Gradle sync to complete

4. **Build the APK**
   
   From Android Studio:
   - Go to Build > Build Bundle(s) / APK(s) > Build APK(s)
   
   Or from command line:
   ```bash
   ./gradlew assembleDebug
   ```

5. **Install on device/emulator**
   
   From Android Studio:
   - Connect your device or start emulator
   - Click the Run button (green triangle)
   
   Or from command line:
   ```bash
   ./gradlew installDebug
   ```

6. **Grant location permissions**
   - On first launch, the app will request location permissions
   - Grant "Allow while using app" or "Allow all the time"
   - This is required for GPS-based weather detection

## 📖 How to Use

### Using the Android App

1. **Launch the App**
   - Open the Weather App from your app drawer
   - You'll see a beautiful splash screen with animation

2. **Get Current Location Weather**
   - The app will automatically request location permission
   - Grant permission to get weather for your current location
   - Weather data will load automatically

3. **Search for a City**
   - Tap the search icon or search bar
   - Type a city name (e.g., "London", "New York", "Tokyo")
   - Or use voice search by tapping the microphone icon
   - Select the city from the dropdown
   - Weather data will load for the selected city

4. **View Hourly Forecast**
   - Scroll down to see the hourly forecast
   - View weather for the next 48 hours
   - See temperature, weather conditions, and precipitation probability

5. **View Daily Forecast**
   - Continue scrolling to see the 7-day forecast
   - View daily high/low temperatures
   - See weather conditions for each day

6. **Refresh Weather**
   - Pull down on the screen to refresh
   - Or tap the refresh icon in the action bar

7. **View Historical Weather**
   - Tap the historical weather icon in the action bar
   - Select start and end dates using the date picker
   - View historical weather data for the selected period

8. **Enable Auto-Updates**
   - The app will check for updates automatically
   - You'll be prompted when an update is available
   - Follow the on-screen instructions to update

### Using the Backend API

#### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

#### Get Current Weather by City
```bash
curl http://localhost:8000/api/v1/weather/city/Bengaluru
```

#### Get Current Weather by Coordinates
```bash
curl "http://localhost:8000/api/v1/weather/coordinates?lat=12.9716&lon=77.5946"
```

#### Get Forecast by City
```bash
curl http://localhost:8000/api/v1/weather/city/Bengaluru/forecast
```

#### Get Forecast by Coordinates
```bash
curl "http://localhost:8000/api/v1/weather/coordinates/forecast?lat=12.9716&lon=77.5946"
```

#### Get Historical Weather
```bash
curl "http://localhost:8000/api/v1/weather/coordinates/historical?lat=12.9716&lon=77.5946&start_date=2024-01-01&end_date=2024-01-31"
```

#### Get Weather Alerts
```bash
curl "http://localhost:8000/api/v1/weather/coordinates/alerts?lat=12.9716&lon=77.5946"
```

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check API health status
- **Response**: JSON with status and timestamp

#### Current Weather
- **Endpoint**: `GET /weather/city/{city}`
- **Description**: Get current weather by city name
- **Parameters**:
  - `city` (path): City name
- **Response**: Current weather data

- **Endpoint**: `GET /weather/coordinates`
- **Description**: Get current weather by coordinates
- **Parameters**:
  - `lat` (query): Latitude (-90 to 90)
  - `lon` (query): Longitude (-180 to 180)
- **Response**: Current weather data

#### Forecast
- **Endpoint**: `GET /weather/city/{city}/forecast`
- **Description**: Get weather forecast by city name
- **Parameters**:
  - `city` (path): City name
- **Response**: Current weather + 48-hour hourly + 7-day daily forecast

- **Endpoint**: `GET /weather/coordinates/forecast`
- **Description**: Get weather forecast by coordinates
- **Parameters**:
  - `lat` (query): Latitude (-90 to 90)
  - `lon` (query): Longitude (-180 to 180)
- **Response**: Current weather + 48-hour hourly + 7-day daily forecast

#### Historical Weather
- **Endpoint**: `GET /weather/coordinates/historical`
- **Description**: Get historical weather data
- **Parameters**:
  - `lat` (query): Latitude (-90 to 90)
  - `lon` (query): Longitude (-180 to 180)
  - `start_date` (query): Start date (YYYY-MM-DD, min 1979-01-01)
  - `end_date` (query): End date (YYYY-MM-DD, max today)
- **Response**: Historical weather data for date range (max 1 year)

#### Weather Alerts
- **Endpoint**: `GET /weather/coordinates/alerts`
- **Description**: Get weather alerts for location
- **Parameters**:
  - `lat` (query): Latitude (-90 to 90)
  - `lon` (query): Longitude (-180 to 180)
- **Response**: List of weather alerts (currently empty - requires integration with official meteorological service)

### Response Formats

#### Current Weather Response
```json
{
  "city": "Bengaluru",
  "country": "IN",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "temperature": 30.8,
  "feels_like": 35.2,
  "humidity": 65,
  "pressure": 1011.8,
  "wind_speed": 12.5,
  "description": "Light drizzle",
  "icon": "09d",
  "sunrise": 1726368480,
  "sunset": 1726411200,
  "timezone": 19800,
  "timezone_id": "Asia/Kolkata"
}
```

#### Forecast Response
```json
{
  "city": "Bengaluru",
  "country": "IN",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "timezone": 19800,
  "timezone_id": "Asia/Kolkata",
  "current": {
    "city": "Bengaluru",
    "country": "IN",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "temperature": 30.8,
    "feels_like": 35.2,
    "humidity": 65,
    "pressure": 1011.8,
    "wind_speed": 12.5,
    "description": "Light drizzle",
    "icon": "09d",
    "sunrise": 1726368480,
    "sunset": 1726411200,
    "timezone": 19800,
    "timezone_id": "Asia/Kolkata"
  },
  "hourly": [
    {
      "time": 1726368000,
      "timezone_offset": 19800,
      "temperature": 30.5,
      "weather_code": 51,
      "weather_description": "Drizzle",
      "weather_icon": "09d",
      "precipitation_probability": 20,
      "precipitation": 0.2
    }
  ],
  "daily": [
    {
      "date": 1726368000,
      "temperature_min": 24.5,
      "temperature_max": 31.2,
      "feels_like_day": 30.1,
      "humidity": 70,
      "pressure": 1012.5,
      "wind_speed": 10.3,
      "weather_description": "Moderate rain",
      "weather_icon": "10d",
      "weather_id": 501,
      "sunrise": 1726368480,
      "sunset": 1726411200
    }
  ]
}
```

#### Historical Weather Response
```json
{
  "latitude": 12.9716,
  "longitude": 77.5946,
  "timezone": "Asia/Kolkata",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "daily": [
    {
      "date": "2024-01-01",
      "temperature_max": 28.4,
      "temperature_min": 16.6,
      "temperature_mean": 21.7,
      "precipitation_sum": 0.0,
      "precipitation_hours": 0.0,
      "wind_speed_max": 19.1,
      "humidity_mean": 66
    }
  ]
}
```

## 🧪 Testing

### Backend Tests

Run all backend tests:
```bash
cd backend
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_weather.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

### Code Quality Checks

Check code style with Ruff:
```bash
cd backend
ruff check app/
```

Format code with Black:
```bash
cd backend
black app/
```

### Android Tests

Run unit tests:
```bash
./gradlew test
```

Run instrumented tests:
```bash
./gradlew connectedAndroidTest
```

### Build Verification

Build debug APK:
```bash
./gradlew assembleDebug
```

Build release APK:
```bash
./gradlew assembleRelease
```

## 🔧 Troubleshooting

### Backend Issues

#### 502 Bad Gateway Error
- **Cause**: Open-Meteo API is down or unreachable
- **Solution**: Check Open-Meteo status at https://open-meteo.com/
- **Alternative**: Wait for API to recover

#### Database Connection Error
- **Cause**: MySQL is not running or credentials are incorrect
- **Solution**:
  ```bash
  # Check MySQL status
  sudo systemctl status mysql  # Linux
  # or
  # Check MySQL service in Windows Services
  
  # Verify credentials in .env file
  # Test connection:
  mysql -u weather_user -p weather_db
  ```

#### Port Already in Use
- **Cause**: Port 8000 is already in use
- **Solution**:
  ```bash
  # Find process using port 8000
  netstat -ano | findstr :8000  # Windows
  lsof -i :8000  # Linux/Mac
  
  # Kill the process or use a different port
  uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
  ```

### Android Issues

#### Connection Refused
- **Cause**: Backend is not running or URL is incorrect
- **Solution**:
  - Verify backend is running: `curl http://localhost:8000/api/v1/health`
  - Check `local.properties` for correct `BACKEND_BASE_URL`
  - For emulator: Use `http://10.0.2.2:8000`
  - For physical device: Use `http://127.0.0.1:8000` and run `adb reverse tcp:8000 tcp:8000`

#### Emulator Network Issues
- **Cause**: Emulator cannot reach host machine
- **Solution**:
  - Use `http://10.0.2.2:8000` in `local.properties`
  - Ensure emulator has internet access
  - Restart emulator if needed

#### Physical Device Network Issues
- **Cause**: Device cannot reach host machine
- **Solution**:
  ```bash
  # Enable USB debugging on device
  # Connect device via USB
  # Verify device is connected
  adb devices
  
  # Reverse port forwarding
  adb reverse tcp:8000 tcp:8000
  
  # Verify forwarding
  adb reverse --list
  ```

#### Build Failures
- **Cause**: JDK version mismatch or Gradle issues
- **Solution**:
  - Ensure JDK 17 is installed: `java -version`
  - Set JAVA_HOME environment variable
  - Clean build: `./gradlew clean`
  - Invalidate caches in Android Studio: File > Invalidate Caches

#### Location Permission Denied
- **Cause**: User denied location permission
- **Solution**:
  - Go to Settings > Apps > Weather App > Permissions
  - Grant Location permission
  - Restart the app

## 🔒 Security

- **No API Keys Required**: Open-Meteo APIs are free and don't require authentication
- **No Secrets in Android**: The Android app contains no API keys or credentials
- **No Direct Database Access**: Android app communicates only via FastAPI
- **HTTPS in Production**: Use HTTPS for production deployments
- **Input Validation**: All inputs validated via Pydantic schemas
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Configuration**: Configurable CORS origins in settings
- **Security Headers**: Built-in security middleware (X-Frame-Options, X-Content-Type-Options, etc.)

## 📊 Data Types

- **Temperature**: Celsius (°C)
- **Pressure**: Hectopascals (hPa) - stored as float
- **Wind Speed**: Meters per second (m/s)
- **Humidity**: Percentage (%)
- **Precipitation**: Millimeters (mm)
- **Sunrise/Sunset**: Unix timestamp (seconds since epoch)
- **Timezone**: Offset in seconds from UTC
- **Coordinates**: Decimal degrees

## 🧭 Testing Status

### ✅ Tested Environments

This app has been thoroughly tested and verified to work correctly on:

#### Real Physical Android Devices
- **Device**: Various Android smartphones
- **Android Versions**: Android 4.4 (API 19) and above
- **Features Tested**:
  - GPS location detection
  - City search functionality
  - Current weather display
  - Hourly forecast (48 hours)
  - Daily forecast (7 days)
  - Historical weather data
  - Swipe to refresh
  - Voice search
  - Auto-update functionality
  - Network connectivity handling
  - Permission handling

#### Android Emulator
- **Emulator**: Android Studio Emulator
- **Android Versions**: Multiple API levels tested
- **Features Tested**:
  - All features listed above
  - Emulator-specific network configuration
  - Port forwarding (10.0.2.2)

### ✅ Test Coverage

- **Backend**: All 21 tests passing
- **Android**: Build successful on all configurations
- **Integration**: Android-FastAPI communication verified
- **API Endpoints**: All endpoints tested and documented
- **Database**: MySQL integration verified
- **Error Handling**: Comprehensive error scenarios tested

### 📹 Test Evidence

Full test results, screenshots, and demo video are available in the `App Screenshots` folder:
- **Demo Video**: `APP WORKING VIDEO.mp4` - Complete app walkthrough
- **Screenshots**: 24 screenshots showing all app features and screens

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests and code quality checks
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

## 📧 Contact

- **GitHub**: [@Skismail57](https://github.com/Skismail57)
- **Repository**: [WeatherApp-Android-FastAPI](https://github.com/Skismail57/WeatherApp-Android-FastAPI)

## 🙏 Acknowledgments

- **Open-Meteo** - For providing free, high-quality weather APIs
- **FastAPI** - For the modern, fast Python web framework
- **Android Team** - For the excellent Android SDK and Material Design
- **Google Play Services** - For location services and app update functionality
- **Lottie** - For beautiful animations
- **Material Design** - For the design system

## 📄 MIT License

Copyright (c) 2026 Skismail57
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
