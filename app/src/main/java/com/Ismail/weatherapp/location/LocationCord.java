package com.Ismail.weatherapp.location;

/**
 * Location coordinates storage class.
 * 
 * The OpenWeather API key has been removed from this class.
 * The Android app now communicates with the FastAPI backend,
 * which handles all OpenWeather API calls server-side.
 * 
 * This class now only stores latitude and longitude coordinates.
 */
public class LocationCord {
    public static String lat = "";
    public static String lon = "";
}

