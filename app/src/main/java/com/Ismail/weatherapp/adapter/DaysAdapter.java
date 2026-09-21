package com.Ismail.weatherapp.adapter;

import android.annotation.SuppressLint;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.Ismail.weatherapp.R;
import com.Ismail.weatherapp.model.DailyWeather;
import com.Ismail.weatherapp.update.UpdateUI;
import com.github.ybq.android.spinkit.SpinKitView;

import java.util.ArrayList;
import java.util.List;

public class DaysAdapter extends RecyclerView.Adapter<DaysAdapter.DayViewHolder> {
    private final Context context;
    private List<DailyWeather> dailyWeatherList;

    public DaysAdapter(Context context) {
        this.context = context;
        this.dailyWeatherList = new ArrayList<>();
    }

    public void setDailyWeatherList(List<DailyWeather> dailyWeatherList) {
        this.dailyWeatherList = dailyWeatherList != null ? dailyWeatherList : new ArrayList<>();
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public DayViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.day_item_layout, parent, false);
        return new DayViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull DayViewHolder holder, int position) {
        if (position < dailyWeatherList.size()) {
            DailyWeather dailyWeather = dailyWeatherList.get(position);
            updateUI(holder, dailyWeather);
            hideProgressBar(holder);
        } else {
            hideProgressBar(holder);
        }
    }

    @Override
    public int getItemCount() {
        return dailyWeatherList.size();
    }

    @SuppressLint("SetTextI18n")
    private void updateUI(DayViewHolder holder, DailyWeather dailyWeather) {
        String day = UpdateUI.TranslateDay(dailyWeather.dayName, context);
        holder.dTime.setText(day);
        
        // Combine min and max temperature into single TextView
        String minTemp = dailyWeather.minTemp != null ? dailyWeather.minTemp : context.getString(R.string.unavailable);
        String maxTemp = dailyWeather.maxTemp != null ? dailyWeather.maxTemp : context.getString(R.string.unavailable);
        holder.temperature.setText(minTemp + "°C / " + maxTemp + "°C");
        
        holder.pressure.setText((dailyWeather.pressure != null ? dailyWeather.pressure : context.getString(R.string.unavailable)) + " mb");
        holder.wind.setText((dailyWeather.windSpeed != null ? dailyWeather.windSpeed : context.getString(R.string.unavailable)) + " km/h");
        holder.humidity.setText((dailyWeather.humidity != null ? dailyWeather.humidity : context.getString(R.string.unavailable)) + "%");
        
        String iconId = UpdateUI.getIconID(dailyWeather.condition, dailyWeather.updateTime, dailyWeather.sunrise, dailyWeather.sunset);
        if (iconId != null) {
            holder.icon.setImageResource(
                    context.getResources().getIdentifier(
                            iconId,
                            "drawable",
                            context.getPackageName()
                    ));
        }
    }

    private void hideProgressBar(DayViewHolder holder) {
        holder.progress.setVisibility(View.GONE);
        holder.layout.setVisibility(View.VISIBLE);
    }

    static class DayViewHolder extends RecyclerView.ViewHolder {
        SpinKitView progress;
        LinearLayout layout;
        TextView dTime, temperature, pressure, wind, humidity;
        ImageView icon;

        public DayViewHolder(@NonNull View itemView) {
            super(itemView);
            progress = itemView.findViewById(R.id.day_progress_bar);
            layout = itemView.findViewById(R.id.day_relative_layout);
            dTime = itemView.findViewById(R.id.day_time);
            temperature = itemView.findViewById(R.id.day_temperature);
            pressure = itemView.findViewById(R.id.day_pressure);
            wind = itemView.findViewById(R.id.day_wind);
            humidity = itemView.findViewById(R.id.day_humidity);
            icon = itemView.findViewById(R.id.day_icon);
        }
    }
}
