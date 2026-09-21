package com.Ismail.weatherapp;

import android.app.DatePickerDialog;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.Ismail.weatherapp.adapter.HistoricalAdapter;
import com.Ismail.weatherapp.model.HistoricalWeatherData;
import com.Ismail.weatherapp.network.WeatherApiClient;
import com.Ismail.weatherapp.toast.Toaster;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class HistoricalWeatherActivity extends AppCompatActivity {
    private static final String TAG = "HistoricalWeatherActivity";
    
    private TextView startDateTv, endDateTv, emptyStateTv;
    private Button fetchButton;
    private ProgressBar progressBar;
    private RecyclerView historicalRv;
    private HistoricalAdapter historicalAdapter;
    
    private Calendar startDateCalendar;
    private Calendar endDateCalendar;
    
    private double latitude;
    private double longitude;
    private String cityName;
    
    private static final String KEY_START_DATE = "start_date";
    private static final String KEY_END_DATE = "end_date";
    private static final String KEY_LATITUDE = "latitude";
    private static final String KEY_LONGITUDE = "longitude";
    private static final String KEY_CITY_NAME = "city_name";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_historical_weather);
        
        // Get coordinates and city name from intent
        latitude = getIntent().getDoubleExtra("latitude", 0);
        longitude = getIntent().getDoubleExtra("longitude", 0);
        cityName = getIntent().getStringExtra("cityName");
        
        if (latitude == 0 || longitude == 0) {
            Toast.makeText(this, "Invalid coordinates", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }
        
        // Initialize views
        startDateTv = findViewById(R.id.start_date_tv);
        endDateTv = findViewById(R.id.end_date_tv);
        emptyStateTv = findViewById(R.id.empty_state_tv);
        fetchButton = findViewById(R.id.fetch_button);
        progressBar = findViewById(R.id.progress_bar);
        historicalRv = findViewById(R.id.historical_rv);
        
        // Initialize calendars
        startDateCalendar = Calendar.getInstance();
        endDateCalendar = Calendar.getInstance();
        
        // Set default date range (last 30 days)
        endDateCalendar.setTime(new Date());
        startDateCalendar.add(Calendar.DAY_OF_MONTH, -30);
        
        updateDateDisplays();
        
        // Set up RecyclerView
        historicalAdapter = new HistoricalAdapter();
        historicalRv.setLayoutManager(new LinearLayoutManager(this));
        historicalRv.setAdapter(historicalAdapter);
        
        // Set up date pickers
        startDateTv.setOnClickListener(v -> showStartDatePicker());
        endDateTv.setOnClickListener(v -> showEndDatePicker());
        
        // Set up fetch button
        fetchButton.setOnClickListener(v -> fetchHistoricalWeather());
        
        // Auto-fetch on load
        fetchHistoricalWeather();
    }
    
    @Override
    protected void onSaveInstanceState(@NonNull Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putLong(KEY_START_DATE, startDateCalendar.getTimeInMillis());
        outState.putLong(KEY_END_DATE, endDateCalendar.getTimeInMillis());
        outState.putDouble(KEY_LATITUDE, latitude);
        outState.putDouble(KEY_LONGITUDE, longitude);
        outState.putString(KEY_CITY_NAME, cityName);
    }
    
    @Override
    protected void onRestoreInstanceState(@NonNull Bundle savedInstanceState) {
        super.onRestoreInstanceState(savedInstanceState);
        startDateCalendar.setTimeInMillis(savedInstanceState.getLong(KEY_START_DATE));
        endDateCalendar.setTimeInMillis(savedInstanceState.getLong(KEY_END_DATE));
        latitude = savedInstanceState.getDouble(KEY_LATITUDE);
        longitude = savedInstanceState.getDouble(KEY_LONGITUDE);
        cityName = savedInstanceState.getString(KEY_CITY_NAME);
        updateDateDisplays();
    }
    
    private void showStartDatePicker() {
        DatePickerDialog datePickerDialog = new DatePickerDialog(
                this,
                (view, year, month, dayOfMonth) -> {
                    startDateCalendar.set(year, month, dayOfMonth);
                    updateDateDisplays();
                },
                startDateCalendar.get(Calendar.YEAR),
                startDateCalendar.get(Calendar.MONTH),
                startDateCalendar.get(Calendar.DAY_OF_MONTH)
        );
        datePickerDialog.getDatePicker().setMaxDate(endDateCalendar.getTimeInMillis());
        datePickerDialog.show();
    }
    
    private void showEndDatePicker() {
        DatePickerDialog datePickerDialog = new DatePickerDialog(
                this,
                (view, year, month, dayOfMonth) -> {
                    endDateCalendar.set(year, month, dayOfMonth);
                    updateDateDisplays();
                },
                endDateCalendar.get(Calendar.YEAR),
                endDateCalendar.get(Calendar.MONTH),
                endDateCalendar.get(Calendar.DAY_OF_MONTH)
        );
        datePickerDialog.getDatePicker().setMinDate(startDateCalendar.getTimeInMillis());
        datePickerDialog.getDatePicker().setMaxDate(new Date().getTime());
        datePickerDialog.show();
    }
    
    private void updateDateDisplays() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH);
        startDateTv.setText(sdf.format(startDateCalendar.getTime()));
        endDateTv.setText(sdf.format(endDateCalendar.getTime()));
    }
    
    private void fetchHistoricalWeather() {
        // Validate coordinates before API request
        if (latitude < -90 || latitude > 90) {
            Log.e(TAG, "Invalid latitude: " + latitude);
            Toaster.errorToast(this, "Invalid coordinates. Please load current weather first.");
            return;
        }
        if (longitude < -180 || longitude > 180) {
            Log.e(TAG, "Invalid longitude: " + longitude);
            Toaster.errorToast(this, "Invalid coordinates. Please load current weather first.");
            return;
        }
        
        Log.d(TAG, "HistoricalWeatherDebug: lat=" + latitude + ", lon=" + longitude + ", startDate=" + startDateCalendar.getTime() + ", endDate=" + endDateCalendar.getTime());
        
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH);
        String startDate = sdf.format(startDateCalendar.getTime());
        String endDate = sdf.format(endDateCalendar.getTime());
        
        // Validate date range (max 1 year)
        long diffInMillis = endDateCalendar.getTimeInMillis() - startDateCalendar.getTimeInMillis();
        long diffInDays = diffInMillis / (1000 * 60 * 60 * 24);
        
        if (diffInDays > 365) {
            Toast.makeText(this, "Date range cannot exceed 1 year", Toast.LENGTH_SHORT).show();
            return;
        }
        
        // Validate minimum date (1979-01-01)
        Calendar minDate = Calendar.getInstance();
        minDate.set(1979, Calendar.JANUARY, 1);
        if (startDateCalendar.before(minDate)) {
            Toast.makeText(this, "Historical data available from 1979-01-01", Toast.LENGTH_SHORT).show();
            return;
        }
        
        progressBar.setVisibility(View.VISIBLE);
        fetchButton.setEnabled(false);
        
        WeatherApiClient weatherApiClient = WeatherApiClient.getInstance(this);
        weatherApiClient.getHistoricalWeatherByCoordinates(latitude, longitude, startDate, endDate, 
                new WeatherApiClient.HistoricalCallback() {
            @Override
            public void onSuccess(WeatherApiClient.HistoricalResponse response) {
                progressBar.setVisibility(View.GONE);
                fetchButton.setEnabled(true);
                
                List<HistoricalWeatherData> dataList = new ArrayList<>();
                for (WeatherApiClient.HistoricalDaily daily : response.daily) {
                    dataList.add(new HistoricalWeatherData(
                            daily.date,
                            daily.temperatureMax,
                            daily.temperatureMin,
                            daily.temperatureMean,
                            daily.precipitationSum,
                            daily.precipitationHours,
                            daily.windSpeedMax,
                            daily.humidityMean
                    ));
                }
                
                if (dataList.isEmpty()) {
                    historicalRv.setVisibility(View.GONE);
                    emptyStateTv.setVisibility(View.VISIBLE);
                } else {
                    historicalRv.setVisibility(View.VISIBLE);
                    emptyStateTv.setVisibility(View.GONE);
                    historicalAdapter.setHistoricalWeatherList(dataList);
                }
                Log.d(TAG, "Historical weather data received: " + dataList.size() + " days");
            }
            
            @Override
            public void onError(String errorMessage) {
                progressBar.setVisibility(View.GONE);
                fetchButton.setEnabled(true);
                Log.e(TAG, "Historical weather request error: " + errorMessage);
                Toaster.errorToast(HistoricalWeatherActivity.this, errorMessage);
            }
        });
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        WeatherApiClient weatherApiClient = WeatherApiClient.getInstance(this);
        weatherApiClient.cancelAllRequests();
    }
}
