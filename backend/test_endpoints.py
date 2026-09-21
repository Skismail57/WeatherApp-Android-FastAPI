"""Manual verification script for FastAPI endpoints.

This script tests the backend endpoints to verify:
1. Weather by city endpoint works
2. Weather by coordinates endpoint works
3. Forecast by city endpoint works
4. Forecast by coordinates endpoint works
"""

import httpx

BASE_URL = "http://localhost:8000"


def test_weather_by_city():
    """Test weather by city endpoint."""
    print("=" * 60)
    print("Testing GET /api/v1/weather/city/{city}")
    print("=" * 60)

    cities = ["Bengaluru", "London", "New York"]

    for city in cities:
        print(f"\nTesting: {city}")
        try:
            response = httpx.get(f"{BASE_URL}/api/v1/weather/city/{city}")
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ City: {data.get('city')}")
                print(f"  ✓ Country: {data.get('country')}")
                print(f"  ✓ Temperature: {data.get('temperature')}°C")
                print(f"  ✓ Description: {data.get('description')}")
                print(f"  ✓ Icon: {data.get('icon')}")
            else:
                print(f"  ✗ Error: {response.text}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")


def test_weather_by_coordinates():
    """Test weather by coordinates endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /api/v1/weather/coordinates")
    print("=" * 60)

    test_coords = [
        (12.9716, 77.5946, "Bengaluru"),
        (51.5074, -0.1278, "London"),
        (40.7128, -74.0060, "New York"),
    ]

    for lat, lon, name in test_coords:
        print(f"\nTesting: {name} ({lat}, {lon})")
        try:
            response = httpx.get(f"{BASE_URL}/api/v1/weather/coordinates", params={"lat": lat, "lon": lon})
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ City: {data.get('city')}")
                print(f"  ✓ Temperature: {data.get('temperature')}°C")
                print(f"  ✓ Description: {data.get('description')}")
            else:
                print(f"  ✗ Error: {response.text}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")


def test_forecast_by_city():
    """Test forecast by city endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /api/v1/weather/city/{city}/forecast")
    print("=" * 60)

    cities = ["Bengaluru", "London"]

    for city in cities:
        print(f"\nTesting: {city}")
        try:
            response = httpx.get(f"{BASE_URL}/api/v1/weather/city/{city}/forecast")
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ City: {data.get('city')}")
                print(f"  ✓ Current Temp: {data.get('current', {}).get('temperature')}°C")
                print(f"  ✓ Daily Forecast Days: {len(data.get('daily', []))}")
                if data.get('daily'):
                    print(f"  ✓ First Day: {data['daily'][0].get('weather_description')}")
            else:
                print(f"  ✗ Error: {response.text}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")


def test_forecast_by_coordinates():
    """Test forecast by coordinates endpoint."""
    print("\n" + "=" * 60)
    print("Testing GET /api/v1/weather/coordinates/forecast")
    print("=" * 60)

    test_coords = [
        (12.9716, 77.5946, "Bengaluru"),
        (51.5074, -0.1278, "London"),
    ]

    for lat, lon, name in test_coords:
        print(f"\nTesting: {name} ({lat}, {lon})")
        try:
            response = httpx.get(f"{BASE_URL}/api/v1/weather/coordinates/forecast", params={"lat": lat, "lon": lon})
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ City: {data.get('city')}")
                print(f"  ✓ Current Temp: {data.get('current', {}).get('temperature')}°C")
                print(f"  ✓ Daily Forecast Days: {len(data.get('daily', []))}")
            else:
                print(f"  ✗ Error: {response.text}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")


def test_error_cases():
    """Test error cases."""
    print("\n" + "=" * 60)
    print("Testing Error Cases")
    print("=" * 60)

    # Invalid city
    print("\nTesting invalid city:")
    try:
        response = httpx.get(f"{BASE_URL}/api/v1/weather/city/InvalidCityName12345")
        print(f"  Status: {response.status_code} (expected 404)")
    except Exception as e:
        print(f"  Exception: {e}")

    # Invalid coordinates
    print("\nTesting invalid coordinates:")
    try:
        response = httpx.get(f"{BASE_URL}/api/v1/weather/coordinates", params={"lat": 91, "lon": 77.5946})
        print(f"  Status: {response.status_code} (expected 422)")
    except Exception as e:
        print(f"  Exception: {e}")


def main():
    """Run all endpoint tests."""
    print("\n" + "=" * 60)
    print("FASTAPI ENDPOINT VERIFICATION")
    print("=" * 60)

    test_weather_by_city()
    test_weather_by_coordinates()
    test_forecast_by_city()
    test_forecast_by_coordinates()
    test_error_cases()

    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
