package com.Ismail.weatherapp.location;

import android.content.Context;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.util.Log;

import java.util.List;
import java.util.Locale;

public class CityFinder {

    public static void setLongitudeLatitude(Location location) {
        try {
            LocationCord.lat = String.valueOf(location.getLatitude());
            LocationCord.lon = String.valueOf(location.getLongitude());
            Log.d("location_lat", LocationCord.lat);
            Log.d("location_lon", LocationCord.lon);
        } catch (NullPointerException e) {
            e.printStackTrace();
        }
    }

    public static String getCityNameUsingNetwork(Context context, Location location) {
        String city = "";
        try {
            Log.d("WeatherDebug", "Reverse geocoding for coordinates: " + location.getLatitude() + ", " + location.getLongitude());
            Geocoder geocoder = new Geocoder(context, Locale.getDefault());
            List<Address> addresses = geocoder.getFromLocation(location.getLatitude(), location.getLongitude(), 1);
            if (addresses != null && !addresses.isEmpty()) {
                Address address = addresses.get(0);
                city = address.getLocality();
                if (city == null || city.isEmpty()) {
                    city = address.getSubAdminArea();
                    Log.d("WeatherDebug", "getLocality null, trying getSubAdminArea: " + city);
                }
                if (city == null || city.isEmpty()) {
                    city = address.getAdminArea();
                    Log.d("WeatherDebug", "getSubAdminArea null, trying getAdminArea: " + city);
                }
                if (city == null || city.isEmpty()) {
                    city = address.getSubLocality();
                    Log.d("WeatherDebug", "getAdminArea null, trying getSubLocality: " + city);
                }
                if (city == null || city.isEmpty()) {
                    city = address.getCountryName();
                    Log.d("WeatherDebug", "getSubLocality null, using getCountryName: " + city);
                }
                Log.d("WeatherDebug", "Geocoder resolved city: " + city);
            } else {
                Log.d("WeatherDebug", "Geocoder: No addresses found for location");
            }
        } catch (Exception e) {
            Log.d("WeatherDebug", "Geocoder error: " + e.getMessage());
        }
        return city;
    }
}
