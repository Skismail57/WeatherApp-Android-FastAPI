package com.Ismail.weatherapp.adapter;

import android.annotation.SuppressLint;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.Ismail.weatherapp.R;
import com.Ismail.weatherapp.model.HourlyWeather;
import com.Ismail.weatherapp.update.UpdateUI;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class HourlyAdapter extends RecyclerView.Adapter<HourlyAdapter.HourlyViewHolder> {
    private final Context context;
    private List<HourlyWeather> hourlyWeatherList;

    public HourlyAdapter(Context context) {
        this.context = context;
        this.hourlyWeatherList = new ArrayList<>();
    }

    public void setHourlyWeatherList(List<HourlyWeather> hourlyWeatherList) {
        this.hourlyWeatherList = hourlyWeatherList != null ? hourlyWeatherList : new ArrayList<>();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public HourlyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.hourly_item_layout, parent, false);
        return new HourlyViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull HourlyViewHolder holder, int position) {
        if (position < hourlyWeatherList.size()) {
            HourlyWeather hourlyWeather = hourlyWeatherList.get(position);
            updateUI(holder, hourlyWeather);
        }
    }

    @Override
    public int getItemCount() {
        return hourlyWeatherList.size();
    }

    @SuppressLint("SetTextI18n")
    private void updateUI(HourlyViewHolder holder, HourlyWeather hourlyWeather) {
        // Format time - Unix timestamp is now correct UTC from backend
        // Use timezone offset to set formatter timezone for display
        long rawTimestamp = hourlyWeather.time;
        int timezoneOffsetSeconds = hourlyWeather.timezoneOffset;
        
        // Create Date from Unix timestamp (absolute instant in UTC)
        Date date = new Date(rawTimestamp * 1000);
        
        // Calculate timezone ID from offset (e.g., 19800s = GMT+05:30)
        int hours = timezoneOffsetSeconds / 3600;
        int minutes = Math.abs((timezoneOffsetSeconds % 3600) / 60);
        String timezoneId = String.format("GMT%+02d:%02d", hours, minutes);
        
        try {
            java.util.TimeZone tz = java.util.TimeZone.getTimeZone(timezoneId);
            SimpleDateFormat timeFormat = new SimpleDateFormat("h a", Locale.ENGLISH);
            timeFormat.setTimeZone(tz);
            String timeStr = timeFormat.format(date);
            
            android.util.Log.d("WeatherDebug", "Hourly timestamp - raw: " + rawTimestamp + ", offset: " + timezoneOffsetSeconds + "s, timezoneId: " + timezoneId + ", converted: " + timeStr);
            
            // Log first 3 records for verification
            if (holder.getAdapterPosition() < 3) {
                android.util.Log.d("WeatherDebug", "Hourly record " + holder.getAdapterPosition() + ": raw timestamp = " + rawTimestamp + ", formatted local time = " + timeStr);
            }
            
            holder.time.setText(timeStr);
        } catch (Exception e) {
            android.util.Log.e("WeatherDebug", "Error formatting hourly time: " + e.getMessage());
            // Fallback to device timezone
            SimpleDateFormat timeFormat = new SimpleDateFormat("h a", Locale.ENGLISH);
            holder.time.setText(timeFormat.format(date));
        }

        // Temperature
        String temp = hourlyWeather.temperature != null ? hourlyWeather.temperature : context.getString(R.string.unavailable);
        holder.temperature.setText(temp + "°C");

        // Precipitation probability
        String precip = hourlyWeather.precipitationProbability != null ? hourlyWeather.precipitationProbability : "0";
        holder.precipitation.setText(precip + "%");

        // Weather icon - use weather icon string directly
        String iconId = hourlyWeather.weatherIcon;
        if (iconId != null) {
            holder.icon.setImageResource(
                    context.getResources().getIdentifier(
                            iconId,
                            "drawable",
                            context.getPackageName()
                    ));
        }
    }

    static class HourlyViewHolder extends RecyclerView.ViewHolder {
        TextView time, temperature, precipitation;
        ImageView icon;

        public HourlyViewHolder(@NonNull View itemView) {
            super(itemView);
            time = itemView.findViewById(R.id.hourly_time);
            temperature = itemView.findViewById(R.id.hourly_temperature);
            precipitation = itemView.findViewById(R.id.hourly_precipitation);
            icon = itemView.findViewById(R.id.hourly_icon);
        }
    }
}
