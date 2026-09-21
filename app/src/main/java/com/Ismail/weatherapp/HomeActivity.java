package com.Ismail.weatherapp;

import static com.Ismail.weatherapp.location.CityFinder.getCityNameUsingNetwork;
import static com.Ismail.weatherapp.location.CityFinder.setLongitudeLatitude;
import static com.Ismail.weatherapp.network.InternetConnectivity.isInternetConnected;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.content.IntentSender;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputMethodManager;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.LinearLayoutManager;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.Ismail.weatherapp.adapter.DaysAdapter;
import com.Ismail.weatherapp.adapter.HourlyAdapter;
import com.Ismail.weatherapp.databinding.ActivityHomeBinding;
import com.Ismail.weatherapp.location.LocationCord;
import com.Ismail.weatherapp.model.DailyWeather;
import com.Ismail.weatherapp.model.HourlyWeather;
import com.Ismail.weatherapp.network.WeatherApiClient;
import com.Ismail.weatherapp.toast.Toaster;
import com.Ismail.weatherapp.update.UpdateUI;
import com.Ismail.weatherapp.url.URL;
import com.Ismail.weatherapp.utils.TimeUtils;
import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.play.core.appupdate.AppUpdateInfo;
import com.google.android.play.core.appupdate.AppUpdateManager;
import com.google.android.play.core.appupdate.AppUpdateManagerFactory;
import com.google.android.play.core.install.model.AppUpdateType;
import com.google.android.play.core.install.model.UpdateAvailability;
import com.google.android.play.core.tasks.Task;

import org.json.JSONException;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.Objects;

public class HomeActivity extends AppCompatActivity {

    private final int WEATHER_FORECAST_APP_UPDATE_REQ_CODE = 101;   // for app update
    private static final int PERMISSION_CODE = 1;                   // for user location permission
    private String name, updated_at, description, temperature, min_temperature, max_temperature, pressure, wind_speed, humidity;
    private int condition;
    private long update_time, sunset, sunrise;
    private String city = "";
    private String timezoneId = "";
    private int timezoneOffset = 0;
    private ActivityHomeBinding binding;
    private RequestQueue requestQueue;
    private DaysAdapter daysAdapter;
    private HourlyAdapter hourlyAdapter;
    private ActivityResultLauncher<Intent> voiceSearchLauncher;
    private boolean weatherLoadStarted = false;
    private android.os.Handler timeUpdateHandler;
    private Runnable timeUpdateRunnable;

    private boolean weatherDataLoaded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d("WeatherDebug", "HomeActivity onCreate started");

        // binding
        binding = ActivityHomeBinding.inflate(getLayoutInflater());
        View view = binding.getRoot();
        setContentView(view);
        
        // Clear search field on start
        binding.searchLayout.cityEt.setText("");
        
        // Initially hide main layout and show loading
        binding.layout.weatherContent.setVisibility(View.GONE);
        binding.progress.setVisibility(View.VISIBLE);
        Log.d("WeatherDebug", "SHOW loading");
        
        Log.d("WeatherDebug", "Views initialized");
        Log.d("WeatherDebug", "Backend base URL = " + BuildConfig.BACKEND_BASE_URL);

        // initialize request queue
        requestQueue = Volley.newRequestQueue(this);

        // initialize days adapter
        daysAdapter = new DaysAdapter(this);
        LinearLayoutManager layoutManager = new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false);
        binding.dayRv.setLayoutManager(layoutManager);
        binding.dayRv.setAdapter(daysAdapter);
        
        // Add spacing between forecast cards
        androidx.recyclerview.widget.RecyclerView.ItemDecoration itemDecoration = new androidx.recyclerview.widget.RecyclerView.ItemDecoration() {
            @Override
            public void getItemOffsets(android.graphics.Rect outRect, android.view.View view, androidx.recyclerview.widget.RecyclerView parent, androidx.recyclerview.widget.RecyclerView.State state) {
                int position = parent.getChildAdapterPosition(view);
                int spanCount = layoutManager.getItemCount();
                if (position < spanCount - 1) {
                    outRect.right = 12; // Space between cards
                }
            }
        };
        binding.dayRv.addItemDecoration(itemDecoration);
        Log.d("WeatherDebug", "DaysAdapter initialized");

        // initialize hourly adapter
        hourlyAdapter = new HourlyAdapter(this);
        LinearLayoutManager hourlyLayoutManager = new LinearLayoutManager(this, LinearLayoutManager.HORIZONTAL, false);
        binding.hourlyRv.setLayoutManager(hourlyLayoutManager);
        binding.hourlyRv.setAdapter(hourlyAdapter);
        Log.d("WeatherDebug", "HourlyAdapter initialized with horizontal LinearLayoutManager");
        
        // Add spacing between hourly cards
        androidx.recyclerview.widget.RecyclerView.ItemDecoration hourlyItemDecoration = new androidx.recyclerview.widget.RecyclerView.ItemDecoration() {
            @Override
            public void getItemOffsets(android.graphics.Rect outRect, android.view.View view, androidx.recyclerview.widget.RecyclerView parent, androidx.recyclerview.widget.RecyclerView.State state) {
                int position = parent.getChildAdapterPosition(view);
                int spanCount = hourlyLayoutManager.getItemCount();
                if (position < spanCount - 1) {
                    outRect.right = 12; // Space between hourly cards
                }
            }
        };
        binding.hourlyRv.addItemDecoration(hourlyItemDecoration);
        Log.d("WeatherDebug", "HourlyAdapter initialized");

        // initialize voice search launcher
        initVoiceSearchLauncher();

        // set navigation bar color
        setNavigationBarColor();

        //check for new app update
        checkUpdate();

        // when user do search and refresh
        listeners();

        // getting data using internet connection
        Log.d("WeatherDebug", "Calling getDataUsingNetwork from onCreate");
        getDataUsingNetwork();
        Log.d("WeatherDebug", "HomeActivity onCreate completed");

    }


    private void initVoiceSearchLauncher() {
        voiceSearchLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    ArrayList<String> arrayList = result.getData().getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                    if (arrayList != null && !arrayList.isEmpty()) {
                        binding.searchLayout.cityEt.setText(arrayList.get(0).toUpperCase());
                        searchCity(binding.searchLayout.cityEt.getText().toString());
                    }
                }
            }
        );
    }


    private void setNavigationBarColor() {
        if (android.os.Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            getWindow().setNavigationBarColor(ContextCompat.getColor(this, R.color.navBarColor));
        }
    }

    private void setUpDaysRecyclerView(List<DailyWeather> dailyWeatherList) {
        if (daysAdapter != null) {
            daysAdapter.setDailyWeatherList(dailyWeatherList);
            binding.dayRv.scrollToPosition(0);
        }
    }

    @SuppressLint("ClickableViewAccessibility")
    private void listeners() {
        binding.layout.weatherContent.setOnTouchListener((view, motionEvent) -> {
            hideKeyboard(view);
            return false;
        });
        binding.searchLayout.searchBarIv.setOnClickListener(view -> searchCity(binding.searchLayout.cityEt.getText().toString()));
        binding.searchLayout.searchBarIv.setOnTouchListener((view, motionEvent) -> {
            hideKeyboard(view);
            return false;
        });
        binding.searchLayout.cityEt.setOnEditorActionListener((textView, i, keyEvent) -> {
            if (i == EditorInfo.IME_ACTION_GO) {
                searchCity(binding.searchLayout.cityEt.getText().toString());
                hideKeyboard(textView);
                return true;
            }
            return false;
        });
        binding.searchLayout.cityEt.setOnFocusChangeListener((view, b) -> {
            if (!b) {
                hideKeyboard(view);
            }
        });
        //Mic Search
        binding.searchLayout.micSearchId.setOnClickListener(view -> {
            Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
            intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak city name");
            try {
                voiceSearchLauncher.launch(intent);
            } catch (android.content.ActivityNotFoundException e) {
                Log.d("Error Voice", "Mic Error:  " + e);
                Toaster.errorToast(this, getString(R.string.weather_data_unavailable));
            }
        });
        //Historical Weather
        binding.historicalCard.setOnClickListener(view -> {
            Intent intent = new Intent(HomeActivity.this, HistoricalWeatherActivity.class);
            // Pass current coordinates from LocationCord
            try {
                double lat = Double.parseDouble(LocationCord.lat);
                double lon = Double.parseDouble(LocationCord.lon);
                intent.putExtra("latitude", lat);
                intent.putExtra("longitude", lon);
                intent.putExtra("cityName", city);
                Log.d("WeatherDebug", "Launching HistoricalWeatherActivity with coordinates: lat=" + lat + ", lon=" + lon + ", city=" + city);
            } catch (NumberFormatException e) {
                Log.e("WeatherDebug", "Failed to parse coordinates for historical weather: " + e.getMessage());
                Toaster.errorToast(this, "Please load current weather first");
            }
            startActivity(intent);
        });
    }

    private void hideKeyboard(View view) {
        InputMethodManager inputMethodManager = (InputMethodManager) view.getContext().getSystemService(Activity.INPUT_METHOD_SERVICE);
        inputMethodManager.hideSoftInputFromWindow(view.getWindowToken(), 0);
    }

    private void checkConnection() {
        Log.d("WeatherDebug", "checkConnection called");
        boolean networkAvailable = isInternetConnected(this);
        Log.d("WeatherDebug", "Network available = " + networkAvailable);
        
        if (!networkAvailable) {
            Log.d("WeatherDebug", "Network unavailable, showing error");
            hideMainLayout();
            Toaster.errorToast(this, getString(R.string.please_check_internet));
        } else {
            Log.d("WeatherDebug", "Network available, calling getDataUsingNetwork");
            getDataUsingNetwork();
        }
    }

    private void searchCity(String cityName) {
        if (cityName == null || cityName.isEmpty()) {
            Toaster.errorToast(this, getString(R.string.please_enter_city_name));
        } else {
            Log.d("WeatherDebug", "City search started for: " + cityName);
            setLatitudeLongitudeUsingCity(cityName);
        }
    }

    private void getDataUsingNetwork() {
        if (weatherLoadStarted) {
            Log.d("WeatherDebug", "Weather load already started, skipping duplicate request");
            return;
        }
        
        weatherLoadStarted = true;
        Log.d("WeatherDebug", "getDataUsingNetwork called");
        FusedLocationProviderClient client = LocationServices.getFusedLocationProviderClient(this);
        
        // Check permission
        boolean hasFineLocation = ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED;
        boolean hasCoarseLocation = ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED;
        
        Log.d("WeatherDebug", "Fine location permission = " + hasFineLocation);
        Log.d("WeatherDebug", "Coarse location permission = " + hasCoarseLocation);
        
        if (!hasFineLocation && !hasCoarseLocation) {
            Log.d("WeatherDebug", "No location permissions, requesting permissions");
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, PERMISSION_CODE);
        } else {
            Log.d("WeatherDebug", "Location permissions granted, requesting current location");
            
            // Try getCurrentLocation first (more reliable)
            try {
                client.getCurrentLocation(com.google.android.gms.location.LocationRequest.PRIORITY_HIGH_ACCURACY, null)
                    .addOnSuccessListener(location -> {
                        Log.d("WeatherDebug", "getCurrentLocation callback received");
                        if (location != null) {
                            handleLocationSuccess(location);
                        } else {
                            Log.d("WeatherDebug", "getCurrentLocation returned null, trying getLastLocation");
                            weatherLoadStarted = false; // Reset guard before fallback
                            Log.d("WeatherDebug", "Resetting weatherLoadStarted flag before getLastLocation fallback");
                            // Fallback to getLastLocation
                            client.getLastLocation().addOnSuccessListener(lastLocation -> {
                                if (lastLocation != null) {
                                    handleLocationSuccess(lastLocation);
                                } else {
                                    Log.d("WeatherDebug", "getLastLocation also returned null");
                                    handleLocationUnavailable();
                                }
                            });
                        }
                    })
                    .addOnFailureListener(e -> {
                        Log.e("WeatherDebug", "getCurrentLocation failed: " + e.getMessage());
                        Log.d("WeatherDebug", "Resetting weatherLoadStarted flag on getCurrentLocation failure");
                        weatherLoadStarted = false; // Reset guard on failure
                        // Fallback to getLastLocation
                        client.getLastLocation().addOnSuccessListener(lastLocation -> {
                            if (lastLocation != null) {
                                handleLocationSuccess(lastLocation);
                            } else {
                                Log.d("WeatherDebug", "getLastLocation failed after getCurrentLocation error");
                                handleLocationUnavailable();
                            }
                        });
                    });
            } catch (SecurityException e) {
                Log.e("WeatherDebug", "Security exception: " + e.getMessage());
                weatherLoadStarted = false; // Reset guard on security exception
                handleLocationUnavailable();
            }
        }
    }
    
    private void handleLocationSuccess(android.location.Location location) {
        double latitude = location.getLatitude();
        double longitude = location.getLongitude();
        
        Log.d("WeatherDebug", "Location received - Lat: " + latitude + ", Lon: " + longitude);
        
        setLongitudeLatitude(location);
        city = getCityNameUsingNetwork(this, location);
        
        Log.d("WeatherDebug", "Detecting city from coordinates");
        if (city == null || city.isEmpty()) {
            city = "Current Location";
            Log.d("WeatherDebug", "Geocoder failed, using 'Current Location' as display name");
        }
        
        Log.d("WeatherDebug", "City detected = " + city);
        
        // Always request weather using coordinates - valid coordinates are available
        Log.d("WeatherDebug", "Requesting weather API for coordinates: " + latitude + ", " + longitude);
        getTodayWeatherInfoByCoordinates(latitude, longitude, city);
    }
    
    private void handleLocationUnavailable() {
        Log.d("WeatherDebug", "Location unavailable - showing manual search prompt");
        weatherLoadStarted = false; // Reset to allow manual search
        Toaster.errorToast(this, "Location unavailable. Search for a city manually.");
        hideProgressBar();
        // Keep weather content hidden when location is unavailable - only search bar should be visible
        binding.layout.weatherContent.setVisibility(View.GONE);
        // Disable NestedScrollView to prevent it from intercepting touch events
        binding.scrollContent.setEnabled(false);
        binding.scrollContent.setFocusable(false);
        binding.scrollContent.setClickable(false);
    }

    @SuppressLint("DefaultLocale")
    private void getTodayWeatherInfoByCoordinates(double lat, double lon, String cityName) {
        Log.d("WeatherDebug", "Weather request started for: " + cityName + " (" + lat + ", " + lon + ")");
        WeatherApiClient weatherApiClient = WeatherApiClient.getInstance(this);
        weatherApiClient.getForecastByCoordinates(lat, lon, new WeatherApiClient.ForecastCallback() {
            @Override
            public void onSuccess(WeatherApiClient.ForecastResponse response) {
                Log.d("WeatherDebug", "Weather API response received");
                try {
                    HomeActivity.this.name = cityName;
                    timezoneId = response.timezoneId;
                    timezoneOffset = response.timezone;
                    
                    // Format updated_at using the selected city's timezone
                    if (timezoneId != null && !timezoneId.isEmpty()) {
                        try {
                            java.time.ZoneId zoneId = java.time.ZoneId.of(timezoneId);
                            java.time.ZonedDateTime cityTime = java.time.ZonedDateTime.now(zoneId);
                            java.time.format.DateTimeFormatter formatter = java.time.format.DateTimeFormatter.ofPattern("EEEE hh:mm a", Locale.ENGLISH);
                            updated_at = cityTime.format(formatter);
                        } catch (Exception e) {
                            // Fallback to device time if timezone parsing fails
                            updated_at = new SimpleDateFormat("EEEE hh:mm a", Locale.ENGLISH).format(new Date());
                        }
                    } else {
                        // Fallback to device time if timezoneId is not available
                        updated_at = new SimpleDateFormat("EEEE hh:mm a", Locale.ENGLISH).format(new Date());
                    }

                    // Map current weather from forecast response
                    WeatherApiClient.WeatherResponse current = response.current;
                    temperature = String.valueOf(Math.round(current.temperature));
                    description = current.description;
                    pressure = String.format("%.1f", current.pressure);
                    wind_speed = String.format("%.1f", current.windSpeed);
                    humidity = String.valueOf(current.humidity);
                    sunrise = current.sunrise;
                    sunset = current.sunset;
                    condition = getConditionIdFromIcon(current.icon);
                    
                    Log.d("HomeActivity_DEBUG", "getTodayWeatherInfoByCoordinates (location) - City: " + cityName + ", timezoneId: " + timezoneId + ", timezoneOffset: " + timezoneOffset + ", sunrise: " + sunrise + ", sunset: " + sunset);
                    
                    // Extract min/max temperature from first day of forecast
                    if (response.daily != null && !response.daily.isEmpty()) {
                        WeatherApiClient.DailyForecast today = response.daily.get(0);
                        min_temperature = String.format("%.0f", today.temperatureMin);
                        max_temperature = String.format("%.0f", today.temperatureMax);
                    } else {
                        min_temperature = null;
                        max_temperature = null;
                    }

                    Log.d("WeatherDebug", "Before updateUI() call");
                    updateUI();
                    Log.d("WeatherDebug", "updateUI completed");
                    hideProgressBar();
                    weatherLoadStarted = false; // Reset guard after successful weather load
                    
                    // Start time updates
                    startTimeUpdates();

                    // Parse and display daily forecast
                    List<DailyWeather> dailyWeatherList = parseForecastResponse(response);
                    if (dailyWeatherList != null && !dailyWeatherList.isEmpty()) {
                        binding.dayRv.setVisibility(View.VISIBLE);
                        daysAdapter.setDailyWeatherList(dailyWeatherList);
                        binding.dayRv.scrollToPosition(0);
                    } else {
                        binding.dayRv.setVisibility(View.GONE);
                    }

                    // Fetch and display weather alerts
                    fetchWeatherAlerts(lat, lon, cityName);

                    // Parse and display hourly forecast
                    List<HourlyWeather> hourlyWeatherList = parseHourlyResponse(response);
                    Log.d("WeatherDebug", "Hourly RecyclerView visibility check - list size: " + hourlyWeatherList.size());
                    Log.d("WeatherDebug", "Hourly RecyclerView initial visibility: " + binding.hourlyRv.getVisibility());
                    if (hourlyWeatherList != null && !hourlyWeatherList.isEmpty()) {
                        binding.hourlyRv.setVisibility(View.VISIBLE);
                        binding.hourlyHeading.setVisibility(View.VISIBLE);
                        hourlyAdapter.setHourlyWeatherList(hourlyWeatherList);
                        binding.hourlyRv.scrollToPosition(0);
                        Log.d("WeatherDebug", "Hourly forecast received: " + hourlyWeatherList.size() + " items, RecyclerView set to VISIBLE");
                        Log.d("WeatherDebug", "Hourly RecyclerView final visibility: " + binding.hourlyRv.getVisibility());
                    } else {
                        binding.hourlyRv.setVisibility(View.GONE);
                        binding.hourlyHeading.setVisibility(View.GONE);
                        Log.d("WeatherDebug", "Hourly forecast empty, RecyclerView set to GONE");
                    }
                } catch (Exception e) {
                    Log.e("WeatherDebug", "Error processing forecast response: " + e.getMessage());
                    weatherLoadStarted = false; // Reset to allow retry
                    Toaster.errorToast(HomeActivity.this, getString(R.string.weather_data_unavailable));
                    hideProgressBar();
                }
            }

            @Override
            public void onError(String errorMessage) {
                Log.e("WeatherDebug", "weather request error: " + errorMessage);
                weatherLoadStarted = false; // Reset to allow retry
                Toaster.errorToast(HomeActivity.this, errorMessage);
                hideProgressBar();
            }
        });
        Log.i("json_req", "Forecast request via FastAPI (coordinates)");
    }

    private void setLatitudeLongitudeUsingCity(String cityName) {
        weatherLoadStarted = false; // Reset guard to allow manual city search
        Log.d("WeatherDebug", "Searching city = " + cityName);
        WeatherApiClient weatherApiClient = WeatherApiClient.getInstance(this);
        weatherApiClient.getWeatherByCity(cityName, new WeatherApiClient.WeatherCallback() {
            @Override
            public void onSuccess(WeatherApiClient.WeatherResponse response) {
                Log.d("WeatherDebug", "City weather response received for: " + response.city);
                LocationCord.lat = String.valueOf(response.latitude);
                LocationCord.lon = String.valueOf(response.longitude);
                getTodayWeatherInfo(cityName);
                binding.searchLayout.cityEt.setText("");
            }

            @Override
            public void onError(String errorMessage) {
                Log.e("WeatherDebug", "City search error = " + errorMessage);
                weatherLoadStarted = false; // Reset to allow retry
                Toaster.errorToast(HomeActivity.this, errorMessage);
                hideProgressBar();
            }
        });
        Log.i("json_req", "Weather request via FastAPI (city)");
    }

    @SuppressLint("DefaultLocale")
    private void getTodayWeatherInfo(String cityName) {
        WeatherApiClient weatherApiClient = WeatherApiClient.getInstance(this);
        weatherApiClient.getForecastByCity(cityName, new WeatherApiClient.ForecastCallback() {
            @Override
            public void onSuccess(WeatherApiClient.ForecastResponse response) {
                try {
                    HomeActivity.this.name = cityName;
                    timezoneId = response.timezoneId;
                    timezoneOffset = response.timezone;
                    
                    // Format updated_at using the selected city's timezone
                    if (timezoneId != null && !timezoneId.isEmpty()) {
                        try {
                            java.time.ZoneId zoneId = java.time.ZoneId.of(timezoneId);
                            java.time.ZonedDateTime cityTime = java.time.ZonedDateTime.now(zoneId);
                            java.time.format.DateTimeFormatter formatter = java.time.format.DateTimeFormatter.ofPattern("EEEE hh:mm a", Locale.ENGLISH);
                            updated_at = cityTime.format(formatter);
                        } catch (Exception e) {
                            // Fallback to device time if timezone parsing fails
                            updated_at = new SimpleDateFormat("EEEE hh:mm a", Locale.ENGLISH).format(new Date());
                        }
                    } else {
                        // Fallback to device time if timezoneId is not available
                        updated_at = new SimpleDateFormat("EEEE hh:mm a", Locale.ENGLISH).format(new Date());
                    }

                    // Map current weather from forecast response
                    WeatherApiClient.WeatherResponse current = response.current;
                    temperature = String.valueOf(Math.round(current.temperature));
                    description = current.description;
                    pressure = String.format("%.1f", current.pressure);
                    wind_speed = String.format("%.1f", current.windSpeed);
                    humidity = String.valueOf(current.humidity);
                    sunrise = current.sunrise;
                    sunset = current.sunset;
                    condition = getConditionIdFromIcon(current.icon);
                    
                    Log.d("HomeActivity_DEBUG", "getTodayWeatherInfo (city search) - City: " + cityName + ", timezoneId: " + timezoneId + ", timezoneOffset: " + timezoneOffset + ", sunrise: " + sunrise + ", sunset: " + sunset);
                    
                    // Extract min/max temperature from first day of forecast
                    if (response.daily != null && !response.daily.isEmpty()) {
                        WeatherApiClient.DailyForecast today = response.daily.get(0);
                        min_temperature = String.format("%.0f", today.temperatureMin);
                        max_temperature = String.format("%.0f", today.temperatureMax);
                    } else {
                        min_temperature = null;
                        max_temperature = null;
                    }

                    Log.d("WeatherDebug", "Before updateUI() call");
                    updateUI();
                    Log.d("WeatherDebug", "updateUI completed");
                    hideProgressBar();
                    weatherLoadStarted = false; // Reset guard after successful weather load
                    
                    // Start time updates
                    startTimeUpdates();

                    // Parse and display daily forecast
                    List<DailyWeather> dailyWeatherList = parseForecastResponse(response);
                    if (dailyWeatherList != null && !dailyWeatherList.isEmpty()) {
                        binding.dayRv.setVisibility(View.VISIBLE);
                        daysAdapter.setDailyWeatherList(dailyWeatherList);
                        binding.dayRv.scrollToPosition(0);
                    } else {
                        binding.dayRv.setVisibility(View.GONE);
                    }

                    // Fetch and display weather alerts
                    fetchWeatherAlerts(response.latitude, response.longitude, cityName);

                    // Parse and display hourly forecast
                    List<HourlyWeather> hourlyWeatherList = parseHourlyResponse(response);
                    Log.d("WeatherDebug", "Hourly RecyclerView visibility check - list size: " + hourlyWeatherList.size());
                    Log.d("WeatherDebug", "Hourly RecyclerView initial visibility: " + binding.hourlyRv.getVisibility());
                    if (hourlyWeatherList != null && !hourlyWeatherList.isEmpty()) {
                        binding.hourlyRv.setVisibility(View.VISIBLE);
                        binding.hourlyHeading.setVisibility(View.VISIBLE);
                        hourlyAdapter.setHourlyWeatherList(hourlyWeatherList);
                        binding.hourlyRv.scrollToPosition(0);
                        Log.d("WeatherDebug", "Hourly forecast received: " + hourlyWeatherList.size() + " items, RecyclerView set to VISIBLE");
                        Log.d("WeatherDebug", "Hourly RecyclerView final visibility: " + binding.hourlyRv.getVisibility());
                    } else {
                        binding.hourlyRv.setVisibility(View.GONE);
                        binding.hourlyHeading.setVisibility(View.GONE);
                        Log.d("WeatherDebug", "Hourly forecast empty, RecyclerView set to GONE");
                    }
                } catch (Exception e) {
                    Log.e("HomeActivity", "Error processing forecast response: " + e.getMessage());
                    weatherLoadStarted = false; // Reset to allow retry
                    Toaster.errorToast(HomeActivity.this, getString(R.string.weather_data_unavailable));
                    hideProgressBar();
                }
            }

            @Override
            public void onError(String errorMessage) {
                Log.e("WeatherDebug", "weather request error: " + errorMessage);
                weatherLoadStarted = false; // Reset to allow retry
                Toaster.errorToast(HomeActivity.this, errorMessage);
                hideProgressBar();
            }
        });
        Log.i("json_req", "Forecast request via FastAPI (city)");
    }

    private int getConditionIdFromIcon(String icon) {
        // Map OpenWeather icon codes to condition IDs
        // This is a simplified mapping - adjust based on actual icon codes
        if (icon == null) return 800;
        
        String iconCode = icon.substring(0, 2); // Get first 2 characters (e.g., "01", "02")
        switch (iconCode) {
            case "01": return 800; // Clear sky
            case "02": return 801; // Few clouds
            case "03": return 802; // Scattered clouds
            case "04": return 803; // Broken clouds
            case "09": return 500; // Shower rain
            case "10": return 501; // Rain
            case "11": return 200; // Thunderstorm
            case "13": return 600; // Snow
            case "50": return 701; // Mist
            default: return 800;
        }
    }

    private List<DailyWeather> parseForecastResponse(WeatherApiClient.ForecastResponse response) {
        List<DailyWeather> dailyWeatherList = new ArrayList<>();
        
        Log.d("HomeActivity_DEBUG", "parseForecastResponse - timezoneId: " + timezoneId + ", response.daily.size(): " + (response.daily != null ? response.daily.size() : 0));
        
        // Get the city's current local date to filter forecast records
        java.time.LocalDate cityToday = null;
        if (timezoneId != null && !timezoneId.isEmpty()) {
            try {
                java.time.ZoneId zoneId = java.time.ZoneId.of(timezoneId);
                cityToday = java.time.ZonedDateTime.now(zoneId).toLocalDate();
                Log.d("HomeActivity_DEBUG", "parseForecastResponse - cityToday: " + cityToday);
            } catch (Exception e) {
                Log.e("HomeActivity", "Error getting city's local date: " + e.getMessage());
            }
        }
        
        // Track which local dates we've already added to prevent duplicates
        java.util.Set<java.time.LocalDate> addedDates = new java.util.HashSet<>();
        
        for (WeatherApiClient.DailyForecast day : response.daily) {
            try {
                // Format day name using the selected city's timezone
                String dayName = "";
                boolean shouldInclude = false;
                java.time.LocalDate forecastDate = null;
                
                if (timezoneId != null && !timezoneId.isEmpty() && cityToday != null) {
                    try {
                        java.time.ZoneId zoneId = java.time.ZoneId.of(timezoneId);
                        // Use Unix timestamp in seconds (backend sends seconds, not milliseconds)
                        java.time.ZonedDateTime cityDateTime = java.time.ZonedDateTime.ofInstant(
                            java.time.Instant.ofEpochSecond(day.date),
                            zoneId
                        );
                        forecastDate = cityDateTime.toLocalDate();
                        
                        Log.d("HomeActivity_DEBUG", "parseForecastResponse - timestamp: " + day.date + ", forecastDate: " + forecastDate + ", cityToday: " + cityToday);
                        
                        // Skip records before the city's local today
                        if (forecastDate.isBefore(cityToday)) {
                            Log.d("HomeActivity_DEBUG", "parseForecastResponse - Skipping record before cityToday");
                            continue;
                        }
                        
                        // Prevent duplicate local dates
                        if (addedDates.contains(forecastDate)) {
                            Log.d("HomeActivity_DEBUG", "parseForecastResponse - Skipping duplicate date: " + forecastDate);
                            continue;
                        }
                        
                        if (forecastDate.equals(cityToday)) {
                            java.time.format.DateTimeFormatter formatter = java.time.format.DateTimeFormatter.ofPattern("EEEE", Locale.ENGLISH);
                            dayName = cityDateTime.format(formatter);
                            shouldInclude = true;
                            Log.d("HomeActivity_DEBUG", "parseForecastResponse - Found TODAY: " + dayName);
                        } else {
                            // forecastDate.isAfter(cityToday) - include future dates
                            java.time.format.DateTimeFormatter formatter = java.time.format.DateTimeFormatter.ofPattern("EEEE", Locale.ENGLISH);
                            dayName = cityDateTime.format(formatter);
                            shouldInclude = true;
                            Log.d("HomeActivity_DEBUG", "parseForecastResponse - Including future date: " + dayName);
                        }
                    } catch (Exception e) {
                        // Fallback to device timezone if city timezone parsing fails
                        dayName = new SimpleDateFormat("EEEE", Locale.ENGLISH).format(new Date(day.date * 1000));
                        shouldInclude = true;
                        Log.e("HomeActivity", "Error parsing forecast date with city timezone, using device timezone: " + e.getMessage());
                    }
                } else {
                    // Fallback to device timezone if timezoneId is not available
                    dayName = new SimpleDateFormat("EEEE", Locale.ENGLISH).format(new Date(day.date * 1000));
                    shouldInclude = true;
                    Log.d("HomeActivity_DEBUG", "parseForecastResponse - Using device timezone fallback: " + dayName);
                }
                
                if (!shouldInclude) {
                    continue;
                }
                
                String minTemp = String.format("%.0f", day.temperatureMin);
                String maxTemp = String.format("%.0f", day.temperatureMax);
                String dayPressure = String.valueOf(day.pressure);
                String dayWind = String.format("%.1f", day.windSpeed);
                String dayHumidity = String.valueOf(day.humidity);
                
                DailyWeather dailyWeather = new DailyWeather(
                    dayName,
                    minTemp,
                    maxTemp,
                    dayPressure,
                    dayWind,
                    dayHumidity,
                    getConditionIdFromIcon(day.weatherIcon),
                    day.sunrise,
                    day.sunset,
                    day.date
                );
                dailyWeatherList.add(dailyWeather);
                
                // Track this date to prevent duplicates
                if (forecastDate != null) {
                    addedDates.add(forecastDate);
                }
                
                // Limit to 7 days of forecast
                if (dailyWeatherList.size() >= 7) {
                    Log.d("HomeActivity_DEBUG", "parseForecastResponse - Reached 7 days limit");
                    break;
                }
            } catch (Exception e) {
                Log.e("HomeActivity", "Error parsing forecast day: " + e.getMessage());
            }
        }
        
        if (dailyWeatherList.isEmpty()) {
            Log.w("HomeActivity", "parseForecastResponse - No forecast records included. cityToday: " + cityToday + ", timezoneId: " + timezoneId);
        } else {
            Log.d("HomeActivity_DEBUG", "parseForecastResponse - Total records included: " + dailyWeatherList.size());
        }
        
        return dailyWeatherList;
    }

    private List<HourlyWeather> parseHourlyResponse(WeatherApiClient.ForecastResponse response) {
        List<HourlyWeather> hourlyWeatherList = new ArrayList<>();
        
        Log.d("WeatherDebug", "parseHourlyResponse called");
        
        if (response.hourly == null || response.hourly.isEmpty()) {
            Log.d("WeatherDebug", "No hourly data in response (null or empty)");
            return hourlyWeatherList;
        }
        
        Log.d("WeatherDebug", "Hourly data count from API = " + response.hourly.size());
        
        for (WeatherApiClient.HourlyForecast hour : response.hourly) {
            try {
                String temp = String.format("%.0f", hour.temperature);
                String precip = String.valueOf(hour.precipitationProbability);
                
                HourlyWeather hourlyWeather = new HourlyWeather(
                    hour.time,
                    hour.timezoneOffset,
                    temp,
                    hour.weatherDescription,
                    hour.weatherIcon,
                    precip
                );
                hourlyWeatherList.add(hourlyWeather);
            } catch (Exception e) {
                Log.e("HomeActivity", "Error parsing hourly forecast: " + e.getMessage());
            }
        }
        
        Log.d("WeatherDebug", "Parsed hourly item count = " + hourlyWeatherList.size());
        return hourlyWeatherList;
    }

    private void fetchWeatherAlerts(double lat, double lon, String cityName) {
        WeatherApiClient weatherApiClient = WeatherApiClient.getInstance(this);
        weatherApiClient.getAlertsByCoordinates(lat, lon, new WeatherApiClient.AlertsCallback() {
            @Override
            public void onSuccess(WeatherApiClient.AlertsResponse alertsResponse) {
                if (alertsResponse.alerts != null && !alertsResponse.alerts.isEmpty()) {
                    binding.alertsHeading.setVisibility(View.VISIBLE);
                    binding.alertsMessage.setVisibility(View.VISIBLE);
                    
                    StringBuilder alertText = new StringBuilder();
                    for (WeatherApiClient.Alert alert : alertsResponse.alerts) {
                        alertText.append("• ").append(alert.title).append("\n");
                    }
                    binding.alertsMessage.setText(alertText.toString());
                    Log.d("WeatherDebug", "Weather alerts received: " + alertsResponse.alerts.size() + " alerts");
                } else {
                    // No official alert source configured - hide alerts section
                    binding.alertsHeading.setVisibility(View.GONE);
                    binding.alertsMessage.setVisibility(View.GONE);
                    Log.d("WeatherDebug", "Weather alerts not configured - no official alert source");
                }
            }

            @Override
            public void onError(String errorMessage) {
                Log.e("WeatherDebug", "Alerts request error: " + errorMessage);
                binding.alertsHeading.setVisibility(View.GONE);
                binding.alertsMessage.setVisibility(View.GONE);
            }
        });
    }

    private void updateUI() {
        Log.d("WeatherDebug", "updateUI - temperature: " + temperature + ", min_temperature: " + min_temperature + ", max_temperature: " + max_temperature);
        Log.d("WeatherDebug", "updateUI - pressure: " + pressure + ", wind_speed: " + wind_speed + ", humidity: " + humidity);
        
        binding.layout.nameTv.setText(name);
        binding.layout.tempTv.setText(temperature + "°C");
        
        if (min_temperature != null && max_temperature != null) {
            binding.layout.minTempTv.setText(min_temperature + "°C");
            binding.layout.maxTempTv.setText(max_temperature + "°C");
            binding.layout.minTempTv.setVisibility(View.VISIBLE);
            binding.layout.maxTempTv.setVisibility(View.VISIBLE);
            Log.d("WeatherDebug", "Min/max TextViews set to VISIBLE with values: " + min_temperature + " / " + max_temperature);
            Log.d("WeatherDebug", "minTempTv visibility: " + binding.layout.minTempTv.getVisibility() + ", alpha: " + binding.layout.minTempTv.getAlpha() + ", text: " + binding.layout.minTempTv.getText());
            Log.d("WeatherDebug", "maxTempTv visibility: " + binding.layout.maxTempTv.getVisibility() + ", alpha: " + binding.layout.maxTempTv.getAlpha() + ", text: " + binding.layout.maxTempTv.getText());
        } else {
            binding.layout.minTempTv.setVisibility(View.GONE);
            binding.layout.maxTempTv.setVisibility(View.GONE);
            Log.d("WeatherDebug", "Min/max TextViews set to GONE (null values)");
        }
        
        binding.layout.conditionDescTv.setText(description);
        binding.layout.pressureTv.setText(pressure + " mb");
        binding.layout.windTv.setText(wind_speed + " km/h");
        binding.layout.humidityTv.setText(humidity + "%");
        binding.layout.updatedAtTv.setText(updated_at);
        
        // Update local time display
        updateLocalTimeDisplay();
        
        Log.d("WeatherDebug", "Pressure/wind/humidity TextViews set: " + pressure + " mb, " + wind_speed + " km/h, " + humidity + "%");
        Log.d("WeatherDebug", "pressureTv visibility: " + binding.layout.pressureTv.getVisibility() + ", alpha: " + binding.layout.pressureTv.getAlpha() + ", text: " + binding.layout.pressureTv.getText());
        Log.d("WeatherDebug", "windTv visibility: " + binding.layout.windTv.getVisibility() + ", alpha: " + binding.layout.windTv.getAlpha() + ", text: " + binding.layout.windTv.getText());
        Log.d("WeatherDebug", "humidityTv visibility: " + binding.layout.humidityTv.getVisibility() + ", alpha: " + binding.layout.humidityTv.getAlpha() + ", text: " + binding.layout.humidityTv.getText());
        
        String iconId = UpdateUI.getIconID(condition, update_time, sunrise, sunset);
        if (iconId != null) {
            binding.layout.conditionIv.setImageResource(
                    getResources().getIdentifier(
                            iconId,
                            "drawable",
                            getPackageName()
                    ));
        }
    }

    private void hideProgressBar() {
        Log.d("WeatherDebug", "HIDE loading");
        binding.progress.setVisibility(View.GONE);
        binding.layout.weatherContent.setVisibility(View.VISIBLE);
        // Enable NestedScrollView when weather data is shown
        binding.scrollContent.setEnabled(true);
        binding.scrollContent.setFocusable(true);
        binding.scrollContent.setClickable(true);
        weatherDataLoaded = true;
    }

    private void hideMainLayout() {
        binding.layout.weatherContent.setVisibility(View.GONE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_CODE) {
            boolean granted = grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED;
            Log.d("LocationDebug", "Permission result: " + granted);
            
            if (granted) {
                Toaster.successToast(this, getString(R.string.permission_granted));
                weatherLoadStarted = false; // Reset guard to allow weather load after permission granted
                getDataUsingNetwork();
            } else {
                Log.d("LocationDebug", "Permission denied");
                weatherLoadStarted = false; // Reset guard to allow manual search
                Toaster.errorToast(this, getString(R.string.permission_denied));
            }
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (requestQueue != null) {
            requestQueue.cancelAll(this);
        }
        WeatherApiClient weatherApiClient = WeatherApiClient.getInstance(this);
        weatherApiClient.cancelAllRequests();
        
        // Stop time updates
        if (timeUpdateHandler != null && timeUpdateRunnable != null) {
            timeUpdateHandler.removeCallbacks(timeUpdateRunnable);
        }
    }

    private void updateLocalTimeDisplay() {
        if (timezoneId != null && !timezoneId.isEmpty()) {
            String dayPeriod = TimeUtils.getDayPeriod(timezoneId, sunrise, sunset);
            String dayPeriodIcon = TimeUtils.getDayPeriodIcon(dayPeriod);
            String formattedTime = TimeUtils.getFormattedLocalTime(timezoneId, timezoneOffset);
            
            if (!formattedTime.isEmpty()) {
                String displayText = dayPeriodIcon + " " + dayPeriod + " · " + formattedTime;
                binding.layout.localTimeTv.setText(displayText);
                binding.layout.localTimeTv.setVisibility(View.VISIBLE);
            } else {
                binding.layout.localTimeTv.setVisibility(View.GONE);
            }
        } else {
            binding.layout.localTimeTv.setVisibility(View.GONE);
        }
    }

    private void startTimeUpdates() {
        if (timeUpdateHandler == null) {
            timeUpdateHandler = new android.os.Handler(android.os.Looper.getMainLooper());
        }
        
        timeUpdateRunnable = new Runnable() {
            @Override
            public void run() {
                updateLocalTimeDisplay();
                // Update every minute
                timeUpdateHandler.postDelayed(this, 60000);
            }
        };
        
        // Start immediate update
        timeUpdateHandler.post(timeUpdateRunnable);
    }

    private void stopTimeUpdates() {
        if (timeUpdateHandler != null && timeUpdateRunnable != null) {
            timeUpdateHandler.removeCallbacks(timeUpdateRunnable);
        }
    }

    @Override
    protected void onResume() {
        
        super.onResume();
        Log.d("WeatherDebug", "onResume called");
        // Reset weather load guard on resume to allow retry
        weatherLoadStarted = false;
        
        // Resume time updates if weather data is loaded
        if (weatherDataLoaded && timezoneId != null && !timezoneId.isEmpty()) {
            startTimeUpdates();
        }
        checkConnection();
    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent event) {
        Log.d("TouchDebug", "action=" + event.getActionMasked() + " x=" + event.getX() + " y=" + event.getY());
        return super.dispatchTouchEvent(event);
    }

    @Override
    protected void onPause() {
        super.onPause();
        // Reset weather load guard on pause to allow retry on resume
        weatherLoadStarted = false;
        Log.d("WeatherDebug", "onPause - reset weatherLoadStarted flag");
    }

    private void checkUpdate() {
        AppUpdateManager appUpdateManager = AppUpdateManagerFactory.create(HomeActivity.this);
        Task<AppUpdateInfo> appUpdateInfoTask = appUpdateManager.getAppUpdateInfo();
        appUpdateInfoTask.addOnSuccessListener(appUpdateInfo -> {
            if (appUpdateInfo.updateAvailability() == UpdateAvailability.UPDATE_AVAILABLE
                    && appUpdateInfo.isUpdateTypeAllowed(AppUpdateType.IMMEDIATE)) {
                try {
                    appUpdateManager.startUpdateFlowForResult(appUpdateInfo, AppUpdateType.IMMEDIATE, HomeActivity.this, WEATHER_FORECAST_APP_UPDATE_REQ_CODE);
                } catch (IntentSender.SendIntentException exception) {
                    Toaster.errorToast(this, getString(R.string.update_failed));
                }
            }
        });
    }

}
