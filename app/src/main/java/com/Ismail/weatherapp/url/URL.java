package com.Ismail.weatherapp.url;

import com.Ismail.weatherapp.location.LocationCord;

/**
 * DEPRECATED: This class previously constructed OpenWeather API URLs directly.
 * 
 * The Android app now uses WeatherApiClient to communicate with the FastAPI backend.
 * The backend handles all OpenWeather API calls.
 * 
 * This class is kept for reference but should not be used for new code.
 * 
 * @deprecated Use {@link com.Ismail.weatherapp.network.WeatherApiClient} instead
 */
@Deprecated
public class URL {
    private String link;
    private static String city_url;

    public URL() {
        // This constructor is no longer used - WeatherApiClient handles API calls
        link = "";
    }

    public String getLink() {
        return link;
    }

    /**
     * @deprecated Use WeatherApiClient.getWeatherByCity() instead
     */
    @Deprecated
    public static void setCity_url(String cityName) {
        // This method is no longer used - WeatherApiClient handles API calls
        city_url = "";
    }

    /**
     * @deprecated Use WeatherApiClient.getWeatherByCity() instead
     */
    @Deprecated
    public static String getCity_url() {
        return city_url;
    }
}
