package com.Ismail.weatherapp.network;

import android.content.Context;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.Ismail.weatherapp.BuildConfig;
import com.Ismail.weatherapp.R;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public class WeatherApiClient {
    private static final String TAG = "WeatherApiClient";
    private static final String WEATHER_ENDPOINT = "/api/v1/weather/city/";
    private static final String WEATHER_COORDINATES_ENDPOINT = "/api/v1/weather/coordinates";
    private static final String FORECAST_ENDPOINT = "/api/v1/weather/city/";
    private static final String FORECAST_COORDINATES_ENDPOINT = "/api/v1/weather/coordinates/forecast";
    private static final String ALERTS_COORDINATES_ENDPOINT = "/api/v1/weather/coordinates/alerts";
    private static final String HISTORICAL_COORDINATES_ENDPOINT = "/api/v1/weather/coordinates/historical";
    private static final int TIMEOUT_MS = 10000;

    private RequestQueue requestQueue;
    private static WeatherApiClient instance;
    private Context context;

    private WeatherApiClient(Context context) {
        this.context = context.getApplicationContext();
        requestQueue = Volley.newRequestQueue(this.context);
    }

    public static synchronized WeatherApiClient getInstance(Context context) {
        if (instance == null) {
            instance = new WeatherApiClient(context);
        }
        return instance;
    }

    public interface WeatherCallback {
        void onSuccess(WeatherResponse response);
        void onError(String errorMessage);
    }

    public interface ForecastCallback {
        void onSuccess(ForecastResponse response);
        void onError(String errorMessage);
    }

    public interface AlertsCallback {
        void onSuccess(AlertsResponse response);
        void onError(String errorMessage);
    }

    public interface HistoricalCallback {
        void onSuccess(HistoricalResponse response);
        void onError(String errorMessage);
    }

    public static class WeatherResponse {
        public String city;
        public String country;
        public double latitude;
        public double longitude;
        public double temperature;
        public double feelsLike;
        public int humidity;
        public double pressure;  // Changed from int to double to match backend
        public double windSpeed;
        public String description;
        public String icon;
        public long sunrise;  // Changed from int to long for Unix timestamp
        public long sunset;   // Changed from int to long for Unix timestamp
        public int timezone;
        public String timezoneId;

        public WeatherResponse(JSONObject json) throws JSONException {
            this.city = json.getString("city");
            this.country = json.getString("country");
            this.latitude = json.getDouble("latitude");
            this.longitude = json.getDouble("longitude");
            this.temperature = json.getDouble("temperature");
            this.feelsLike = json.getDouble("feels_like");
            this.humidity = json.getInt("humidity");
            this.pressure = json.getDouble("pressure");  // Changed to getDouble
            this.windSpeed = json.getDouble("wind_speed");
            this.description = json.getString("description");
            this.icon = json.getString("icon");
            this.sunrise = json.optLong("sunrise", 0);  // Changed to optLong
            this.sunset = json.optLong("sunset", 0);    // Changed to optLong
            this.timezone = json.optInt("timezone", 0);
            this.timezoneId = json.optString("timezone_id", "");
            Log.d("WeatherApiClient_DEBUG", "WeatherResponse parsed - city: " + this.city + ", timezoneId: " + this.timezoneId + ", timezoneOffset: " + this.timezone + ", sunrise: " + this.sunrise + ", sunset: " + this.sunset);
        }
    }

    public static class ForecastResponse {
        public String city;
        public String country;
        public double latitude;
        public double longitude;
        public int timezone;
        public String timezoneId;
        public WeatherResponse current;
        public java.util.List<HourlyForecast> hourly;
        public java.util.List<DailyForecast> daily;

        public ForecastResponse(JSONObject json) throws JSONException {
            this.city = json.getString("city");
            this.country = json.getString("country");
            this.latitude = json.getDouble("latitude");
            this.longitude = json.getDouble("longitude");
            this.timezone = json.getInt("timezone");
            this.timezoneId = json.optString("timezone_id", "");
            Log.d("WeatherApiClient_DEBUG", "ForecastResponse parsed - city: " + this.city + ", timezoneId: " + this.timezoneId + ", timezoneOffset: " + this.timezone);

            JSONObject currentJson = json.getJSONObject("current");
            this.current = new WeatherResponse(currentJson);

            this.hourly = new java.util.ArrayList<>();
            if (json.has("hourly")) {
                org.json.JSONArray hourlyArray = json.getJSONArray("hourly");
                Log.d("WeatherDebug", "Hourly JSON received, item count = " + hourlyArray.length());
                for (int i = 0; i < hourlyArray.length(); i++) {
                    this.hourly.add(new HourlyForecast(hourlyArray.getJSONObject(i)));
                }
            } else {
                Log.d("WeatherDebug", "Hourly JSON NOT found in response");
            }

            this.daily = new java.util.ArrayList<>();
            org.json.JSONArray dailyArray = json.getJSONArray("daily");
            for (int i = 0; i < dailyArray.length(); i++) {
                this.daily.add(new DailyForecast(dailyArray.getJSONObject(i)));
            }
        }
    }

    public static class DailyForecast {
        public int date;
        public double temperatureMin;
        public double temperatureMax;
        public double feelsLikeDay;
        public int humidity;
        public double pressure;  // Changed from int to double to match backend
        public double windSpeed;
        public String weatherDescription;
        public String weatherIcon;
        public int weatherId;
        public long sunrise;  // Changed from int to long for Unix timestamp
        public long sunset;   // Changed from int to long for Unix timestamp

        public DailyForecast(JSONObject json) throws JSONException {
            this.date = json.getInt("date");
            this.temperatureMin = json.getDouble("temperature_min");
            this.temperatureMax = json.getDouble("temperature_max");
            this.feelsLikeDay = json.getDouble("feels_like_day");
            this.humidity = json.getInt("humidity");
            this.pressure = json.getDouble("pressure");  // Changed to getDouble
            this.windSpeed = json.getDouble("wind_speed");
            this.weatherDescription = json.getString("weather_description");
            this.weatherIcon = json.getString("weather_icon");
            this.weatherId = json.getInt("weather_id");
            this.sunrise = json.optLong("sunrise", 0);  // Changed to optLong
            this.sunset = json.optLong("sunset", 0);    // Changed to optLong
        }
    }

    public static class HourlyForecast {
        public long time;
        public int timezoneOffset;
        public double temperature;
        public int weatherCode;
        public String weatherDescription;
        public String weatherIcon;
        public int precipitationProbability;
        public double precipitation;

        public HourlyForecast(JSONObject json) throws JSONException {
            this.time = json.getLong("time");
            this.timezoneOffset = json.optInt("timezone_offset", 0);
            this.temperature = json.getDouble("temperature");
            this.weatherCode = json.getInt("weather_code");
            this.weatherDescription = json.getString("weather_description");
            this.weatherIcon = json.getString("weather_icon");
            this.precipitationProbability = json.optInt("precipitation_probability", 0);
            this.precipitation = json.optDouble("precipitation", 0);
        }
    }

    public void getWeatherByCity(String cityName, WeatherCallback callback) {
        if (cityName == null || cityName.trim().isEmpty()) {
            callback.onError("City name cannot be empty");
            return;
        }

        String encodedCityName = URLEncoder.encode(cityName.trim(), StandardCharsets.UTF_8).replace("+", "%20");
        String url = BuildConfig.BACKEND_BASE_URL + WEATHER_ENDPOINT + encodedCityName;

        Log.d(TAG, "Requesting weather from: " + url);
        Log.d("WeatherDebug", "City weather API URL = " + url);

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                response -> {
                    try {
                        WeatherResponse weatherResponse = new WeatherResponse(response);
                        callback.onSuccess(weatherResponse);
                        Log.d(TAG, "Weather data received for: " + weatherResponse.city);
                    } catch (JSONException e) {
                        Log.e(TAG, "Failed to parse weather response: " + e.getMessage());
                        callback.onError("Failed to parse weather data");
                    }
                },
                error -> {
                    String errorMessage = parseVolleyError(error);
                    Log.e(TAG, "Weather request failed: " + errorMessage);
                    callback.onError(errorMessage);
                }
        );

        request.setRetryPolicy(new com.android.volley.DefaultRetryPolicy(
                TIMEOUT_MS,
                com.android.volley.DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                com.android.volley.DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        requestQueue.add(request);
    }

    public void getWeatherByCoordinates(double lat, double lon, WeatherCallback callback) {
        String url = BuildConfig.BACKEND_BASE_URL + WEATHER_COORDINATES_ENDPOINT + "?lat=" + lat + "&lon=" + lon;

        Log.d(TAG, "Requesting weather from: " + url);

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                response -> {
                    try {
                        WeatherResponse weatherResponse = new WeatherResponse(response);
                        callback.onSuccess(weatherResponse);
                        Log.d(TAG, "Weather data received for coordinates: " + lat + ", " + lon);
                    } catch (JSONException e) {
                        Log.e(TAG, "Failed to parse weather response: " + e.getMessage());
                        callback.onError("Failed to parse weather data");
                    }
                },
                error -> {
                    String errorMessage = parseVolleyError(error);
                    Log.e(TAG, "Weather request failed: " + errorMessage);
                    callback.onError(errorMessage);
                }
        );

        request.setRetryPolicy(new com.android.volley.DefaultRetryPolicy(
                TIMEOUT_MS,
                com.android.volley.DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                com.android.volley.DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        requestQueue.add(request);
    }

    public void getForecastByCity(String cityName, ForecastCallback callback) {
        if (cityName == null || cityName.trim().isEmpty()) {
            callback.onError("City name cannot be empty");
            return;
        }

        String encodedCityName = URLEncoder.encode(cityName.trim(), StandardCharsets.UTF_8).replace("+", "%20");
        String url = BuildConfig.BACKEND_BASE_URL + FORECAST_ENDPOINT + encodedCityName + "/forecast";

        Log.d(TAG, "Requesting forecast from: " + url);

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                response -> {
                    try {
                        ForecastResponse forecastResponse = new ForecastResponse(response);
                        callback.onSuccess(forecastResponse);
                        Log.d(TAG, "Forecast data received for: " + forecastResponse.city);
                    } catch (JSONException e) {
                        Log.e(TAG, "Failed to parse forecast response: " + e.getMessage());
                        callback.onError("Failed to parse forecast data");
                    }
                },
                error -> {
                    String errorMessage = parseVolleyError(error);
                    Log.e(TAG, "Forecast request failed: " + errorMessage);
                    callback.onError(errorMessage);
                }
        );

        request.setRetryPolicy(new com.android.volley.DefaultRetryPolicy(
                TIMEOUT_MS,
                com.android.volley.DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                com.android.volley.DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        requestQueue.add(request);
    }

    public void getForecastByCoordinates(double lat, double lon, ForecastCallback callback) {
        String url = BuildConfig.BACKEND_BASE_URL + FORECAST_COORDINATES_ENDPOINT + "?lat=" + lat + "&lon=" + lon;

        Log.d(TAG, "Requesting forecast from: " + url);

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                response -> {
                    try {
                        ForecastResponse forecastResponse = new ForecastResponse(response);
                        callback.onSuccess(forecastResponse);
                        Log.d(TAG, "Forecast data received for coordinates: " + lat + ", " + lon);
                    } catch (JSONException e) {
                        Log.e(TAG, "Failed to parse forecast response: " + e.getMessage());
                        callback.onError("Failed to parse forecast data");
                    }
                },
                error -> {
                    String errorMessage = parseVolleyError(error);
                    Log.e(TAG, "Forecast request failed: " + errorMessage);
                    callback.onError(errorMessage);
                }
        );

        request.setRetryPolicy(new com.android.volley.DefaultRetryPolicy(
                TIMEOUT_MS,
                com.android.volley.DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                com.android.volley.DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        requestQueue.add(request);
    }

    public void getAlertsByCoordinates(double lat, double lon, AlertsCallback callback) {
        String url = BuildConfig.BACKEND_BASE_URL + ALERTS_COORDINATES_ENDPOINT + "?lat=" + lat + "&lon=" + lon;

        Log.d(TAG, "Requesting alerts from: " + url);

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                response -> {
                    try {
                        AlertsResponse alertsResponse = new AlertsResponse(response);
                        callback.onSuccess(alertsResponse);
                        Log.d(TAG, "Alerts data received for coordinates: " + lat + ", " + lon);
                    } catch (JSONException e) {
                        Log.e(TAG, "Failed to parse alerts response: " + e.getMessage());
                        callback.onError("Failed to parse alerts data");
                    }
                },
                error -> {
                    String errorMessage = parseVolleyError(error);
                    Log.e(TAG, "Alerts request failed: " + errorMessage);
                    callback.onError(errorMessage);
                }
        );

        request.setRetryPolicy(new com.android.volley.DefaultRetryPolicy(
                TIMEOUT_MS,
                com.android.volley.DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                com.android.volley.DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        requestQueue.add(request);
    }

    public void getHistoricalWeatherByCoordinates(double lat, double lon, String startDate, String endDate, HistoricalCallback callback) {
        String url = BuildConfig.BACKEND_BASE_URL + HISTORICAL_COORDINATES_ENDPOINT + "?lat=" + lat + "&lon=" + lon + "&start_date=" + startDate + "&end_date=" + endDate;

        Log.d(TAG, "Requesting historical weather from: " + url);

        JsonObjectRequest request = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                response -> {
                    try {
                        HistoricalResponse historicalResponse = new HistoricalResponse(response);
                        callback.onSuccess(historicalResponse);
                        Log.d(TAG, "Historical weather data received for coordinates: " + lat + ", " + lon);
                    } catch (JSONException e) {
                        Log.e(TAG, "Failed to parse historical weather response: " + e.getMessage());
                        callback.onError("Failed to parse historical weather data");
                    }
                },
                error -> {
                    String errorMessage = parseVolleyError(error);
                    Log.e(TAG, "Historical weather request failed: " + errorMessage);
                    callback.onError(errorMessage);
                }
        );

        request.setRetryPolicy(new com.android.volley.DefaultRetryPolicy(
                TIMEOUT_MS,
                com.android.volley.DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                com.android.volley.DefaultRetryPolicy.DEFAULT_BACKOFF_MULT
        ));

        requestQueue.add(request);
    }

    public static class AlertsResponse {
        public String city;
        public String country;
        public double latitude;
        public double longitude;
        public java.util.List<Alert> alerts;

        public AlertsResponse(JSONObject json) throws JSONException {
            this.city = json.optString("city", "Unknown");
            this.country = json.optString("country", "");
            this.latitude = json.getDouble("latitude");
            this.longitude = json.getDouble("longitude");

            this.alerts = new java.util.ArrayList<>();
            if (json.has("alerts")) {
                org.json.JSONArray alertsArray = json.getJSONArray("alerts");
                for (int i = 0; i < alertsArray.length(); i++) {
                    this.alerts.add(new Alert(alertsArray.getJSONObject(i)));
                }
            }
        }
    }

    public static class Alert {
        public String id;
        public String title;
        public String description;
        public String severity;
        public String area;
        public long effectiveTime;
        public long expiresTime;
        public String source;
        public String sourceUrl;

        public Alert(JSONObject json) throws JSONException {
            this.id = json.getString("id");
            this.title = json.getString("title");
            this.description = json.getString("description");
            this.severity = json.getString("severity");
            this.area = json.getString("area");
            this.effectiveTime = json.getLong("effective_time");
            this.expiresTime = json.getLong("expires_time");
            this.source = json.getString("source");
            this.sourceUrl = json.optString("source_url", "");
        }
    }

    public static class HistoricalResponse {
        public double latitude;
        public double longitude;
        public String timezone;
        public String startDate;
        public String endDate;
        public java.util.List<HistoricalDaily> daily;

        public HistoricalResponse(JSONObject json) throws JSONException {
            this.latitude = json.getDouble("latitude");
            this.longitude = json.getDouble("longitude");
            this.timezone = json.getString("timezone");
            this.startDate = json.getString("start_date");
            this.endDate = json.getString("end_date");

            this.daily = new java.util.ArrayList<>();
            if (json.has("daily")) {
                org.json.JSONArray dailyArray = json.getJSONArray("daily");
                for (int i = 0; i < dailyArray.length(); i++) {
                    this.daily.add(new HistoricalDaily(dailyArray.getJSONObject(i)));
                }
            }
        }
    }

    public static class HistoricalDaily {
        public String date;
        public double temperatureMax;
        public double temperatureMin;
        public double temperatureMean;
        public double precipitationSum;
        public double precipitationHours;
        public double windSpeedMax;
        public double humidityMean;

        public HistoricalDaily(JSONObject json) throws JSONException {
            this.date = json.optString("date", "");
            this.temperatureMax = json.optDouble("temperature_max", 0.0);
            this.temperatureMin = json.optDouble("temperature_min", 0.0);
            this.temperatureMean = json.optDouble("temperature_mean", 0.0);
            this.precipitationSum = json.optDouble("precipitation_sum", 0.0);
            this.precipitationHours = json.optDouble("precipitation_hours", 0.0);
            this.windSpeedMax = json.optDouble("wind_speed_max", 0.0);
            this.humidityMean = json.optDouble("humidity_mean", 0.0);
        }
    }

    private String parseVolleyError(VolleyError error) {
        if (error.networkResponse != null) {
            int statusCode = error.networkResponse.statusCode;
            switch (statusCode) {
                case 400:
                    return "Invalid city name";
                case 404:
                    return "City not found";
                case 429:
                    return "Too many requests. Please try again later";
                case 500:
                    return "Weather service not configured";
                case 502:
                    return "Weather service unavailable";
                case 503:
                    return "Weather service timeout";
                default:
                    return "Server error: " + statusCode;
            }
        }

        if (error instanceof com.android.volley.TimeoutError) {
            return "Request timeout. Please check your connection";
        }

        if (error instanceof com.android.volley.NoConnectionError) {
            return context.getString(R.string.network_connection_error);
        }

        if (error instanceof com.android.volley.NetworkError) {
            return context.getString(R.string.network_connection_error);
        }

        return "Failed to fetch weather data";
    }

    public void cancelAllRequests() {
        if (requestQueue != null) {
            requestQueue.cancelAll(TAG);
        }
    }
}
