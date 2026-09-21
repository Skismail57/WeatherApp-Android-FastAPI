"""Simple test of FastAPI endpoints."""

import httpx
import time

BASE_URL = "http://localhost:8002"

# Wait for server to be ready
time.sleep(2)

print("Testing FastAPI endpoints...")

# Test health
try:
    response = httpx.get(f"{BASE_URL}/api/v1/health", timeout=5.0)
    print(f"Health: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Health failed: {e}")

# Test weather by city
try:
    response = httpx.get(f"{BASE_URL}/api/v1/weather/city/Bengaluru", timeout=30.0)
    print(f"Weather by city: {response.status_code}")
    if response.status_code == 200:
        print(f"  Data: {response.json()}")
    else:
        print(f"  Error: {response.text}")
except Exception as e:
    print(f"Weather by city failed: {e}")

# Test forecast by city
try:
    response = httpx.get(f"{BASE_URL}/api/v1/weather/city/Bengaluru/forecast", timeout=30.0)
    print(f"Forecast by city: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  City: {data.get('city')}")
        print(f"  Current temp: {data.get('current', {}).get('temperature')}")
        print(f"  Daily days: {len(data.get('daily', []))}")
    else:
        print(f"  Error: {response.text}")
except Exception as e:
    print(f"Forecast by city failed: {e}")

print("Done.")
