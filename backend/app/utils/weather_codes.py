"""WMO Weather Code mapping utilities for Open-Meteo API integration.

Open-Meteo uses WMO weather codes to describe weather conditions.
This module provides mapping functions to convert WMO codes to
human-readable descriptions and icon codes compatible with the Android app.
"""

# WMO weather code to description mapping
WMO_CODE_DESCRIPTIONS: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# WMO code to OpenWeather-like icon code mapping
# Maps WMO codes to icon codes compatible with the existing Android icon system
WMO_CODE_TO_ICON: dict[int, str] = {
    0: "01d",  # Clear sky - day
    1: "02d",  # Mainly clear - day
    2: "03d",  # Partly cloudy - day
    3: "04d",  # Overcast
    45: "50d",  # Fog
    48: "50d",  # Depositing rime fog
    51: "09d",  # Light drizzle
    53: "09d",  # Moderate drizzle
    55: "09d",  # Dense drizzle
    56: "09d",  # Light freezing drizzle
    57: "09d",  # Dense freezing drizzle
    61: "10d",  # Slight rain
    63: "10d",  # Moderate rain
    65: "10d",  # Heavy rain
    66: "10d",  # Light freezing rain
    67: "10d",  # Heavy freezing rain
    71: "13d",  # Slight snow fall
    73: "13d",  # Moderate snow fall
    75: "13d",  # Heavy snow fall
    77: "13d",  # Snow grains
    80: "09d",  # Slight rain showers
    81: "09d",  # Moderate rain showers
    82: "09d",  # Violent rain showers
    85: "13d",  # Slight snow showers
    86: "13d",  # Heavy snow showers
    95: "11d",  # Thunderstorm
    96: "11d",  # Thunderstorm with slight hail
    99: "11d",  # Thunderstorm with heavy hail
}

# Night icon variants (replace 'd' with 'n')
WMO_CODE_TO_ICON_NIGHT: dict[int, str] = {
    code: icon.replace("d", "n") for code, icon in WMO_CODE_TO_ICON.items()
}


def weather_code_to_description(code: int) -> str:
    """Convert WMO weather code to human-readable description.

    Args:
        code: WMO weather code (0-99)

    Returns:
        Human-readable weather description
    """
    return WMO_CODE_DESCRIPTIONS.get(code, "Unknown")


def weather_code_to_icon(code: int, is_day: bool = True) -> str:
    """Convert WMO weather code to icon code.

    Args:
        code: WMO weather code (0-99)
        is_day: Whether it's daytime (True) or nighttime (False)

    Returns:
        Icon code compatible with Android app (e.g., "01d", "01n")
    """
    icon_mapping = WMO_CODE_TO_ICON if is_day else WMO_CODE_TO_ICON_NIGHT
    return icon_mapping.get(code, "01d" if is_day else "01n")


def weather_code_to_condition_id(code: int) -> int:
    """Convert WMO weather code to OpenWeather-like condition ID.

    This maps WMO codes to condition IDs that the Android app expects
    for icon selection logic.

    Args:
        code: WMO weather code (0-99)

    Returns:
        OpenWeather-like condition ID
    """
    # Map WMO codes to OpenWeather condition IDs
    # This is a simplified mapping for the existing Android icon system
    mapping = {
        0: 800,  # Clear sky
        1: 801,  # Mainly clear
        2: 802,  # Partly cloudy
        3: 803,  # Overcast
        45: 701,  # Fog
        48: 701,  # Depositing rime fog
        51: 300,  # Light drizzle
        53: 301,  # Moderate drizzle
        55: 302,  # Dense drizzle
        56: 511,  # Light freezing drizzle
        57: 511,  # Dense freezing drizzle
        61: 500,  # Slight rain
        63: 501,  # Moderate rain
        65: 502,  # Heavy rain
        66: 511,  # Light freezing rain
        67: 511,  # Heavy freezing rain
        71: 600,  # Slight snow fall
        73: 601,  # Moderate snow fall
        75: 602,  # Heavy snow fall
        77: 601,  # Snow grains
        80: 520,  # Slight rain showers
        81: 521,  # Moderate rain showers
        82: 522,  # Violent rain showers
        85: 620,  # Slight snow showers
        86: 622,  # Heavy snow showers
        95: 200,  # Thunderstorm
        96: 200,  # Thunderstorm with slight hail
        99: 200,  # Thunderstorm with heavy hail
    }
    return mapping.get(code, 800)  # Default to clear sky
