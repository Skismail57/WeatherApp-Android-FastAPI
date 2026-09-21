"""Test FastAPI endpoints with real Open-Meteo to diagnose 502 issue."""

import httpx

BASE_URL = "http://localhost:8000"


def test_root():
    """Test root endpoint."""
    print("=" * 60)
    print("Testing GET /")
    print("=" * 60)
    try:
        response = httpx.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:100]}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


def test_health():
    """Test health endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /api/v1/health")
    print("=" * 60)
    try:
        response = httpx.get(f"{BASE_URL}/api/v1/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:100]}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


def test_weather_by_city():
    """Test weather by city endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /api/v1/weather/city/Bengaluru")
    print("=" * 60)
    try:
        response = httpx.get(f"{BASE_URL}/api/v1/weather/city/Bengaluru")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ City: {data.get('city')}")
            print(f"✓ Temperature: {data.get('temperature')}°C")
            print(f"✓ Description: {data.get('description')}")
            return True
        else:
            print(f"✗ Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


def test_forecast_by_city():
    """Test forecast by city endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /api/v1/weather/city/Bengaluru/forecast")
    print("=" * 60)
    try:
        response = httpx.get(f"{BASE_URL}/api/v1/weather/city/Bengaluru/forecast", timeout=30.0)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ City: {data.get('city')}")
            print(f"✓ Current Temp: {data.get('current', {}).get('temperature')}°C")
            print(f"✓ Daily Days: {len(data.get('daily', []))}")
            return True
        else:
            print(f"✗ Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


def test_weather_by_coordinates():
    """Test weather by coordinates endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /api/v1/weather/coordinates")
    print("=" * 60)
    try:
        response = httpx.get(f"{BASE_URL}/api/v1/weather/coordinates", params={"lat": 12.9716, "lon": 77.5946})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ City: {data.get('city')}")
            print(f"✓ Temperature: {data.get('temperature')}°C")
            return True
        else:
            print(f"✗ Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


def main():
    """Run all endpoint tests."""
    print("\n" + "=" * 60)
    print("FASTAPI ENDPOINT TEST")
    print("=" * 60)
    
    results = {
        "Root": test_root(),
        "Health": test_health(),
        "Weather by City": test_weather_by_city(),
        "Forecast by City": test_forecast_by_city(),
        "Weather by Coordinates": test_weather_by_coordinates(),
    }
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for test, result in results.items():
        print(f"{test}: {'PASS' if result else 'FAIL'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
