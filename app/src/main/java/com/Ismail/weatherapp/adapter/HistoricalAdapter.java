package com.Ismail.weatherapp.adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.Ismail.weatherapp.R;
import com.Ismail.weatherapp.model.HistoricalWeatherData;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class HistoricalAdapter extends RecyclerView.Adapter<HistoricalAdapter.HistoricalViewHolder> {
    private List<HistoricalWeatherData> historicalWeatherList;

    public void setHistoricalWeatherList(List<HistoricalWeatherData> historicalWeatherList) {
        this.historicalWeatherList = historicalWeatherList;
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public HistoricalViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_historical_weather, parent, false);
        return new HistoricalViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull HistoricalViewHolder holder, int position) {
        if (historicalWeatherList == null || position >= historicalWeatherList.size()) {
            return;
        }
        
        HistoricalWeatherData data = historicalWeatherList.get(position);
        if (data == null) {
            return;
        }
        
        try {
            SimpleDateFormat inputFormat = new SimpleDateFormat("yyyy-MM-dd", Locale.ENGLISH);
            SimpleDateFormat outputFormat = new SimpleDateFormat("MMM dd, yyyy", Locale.ENGLISH);
            Date date = inputFormat.parse(data.date);
            holder.dateTv.setText(outputFormat.format(date));
        } catch (Exception e) {
            holder.dateTv.setText(data.date != null ? data.date : "N/A");
        }
        
        holder.tempMaxTv.setText(String.format("%.1f°C", data.temperatureMax));
        holder.tempMinTv.setText(String.format("%.1f°C", data.temperatureMin));
        holder.tempMeanTv.setText(String.format("%.1f°C", data.temperatureMean));
        holder.precipTv.setText(String.format("%.1f mm", data.precipitationSum));
        holder.windTv.setText(String.format("%.1f km/h", data.windSpeedMax));
        holder.humidityTv.setText(String.format("%.0f%%", data.humidityMean));
    }

    @Override
    public int getItemCount() {
        return historicalWeatherList != null ? historicalWeatherList.size() : 0;
    }

    static class HistoricalViewHolder extends RecyclerView.ViewHolder {
        TextView dateTv, tempMaxTv, tempMinTv, tempMeanTv, precipTv, windTv, humidityTv;

        public HistoricalViewHolder(@NonNull View itemView) {
            super(itemView);
            dateTv = itemView.findViewById(R.id.historical_date);
            tempMaxTv = itemView.findViewById(R.id.historical_temp_max);
            tempMinTv = itemView.findViewById(R.id.historical_temp_min);
            tempMeanTv = itemView.findViewById(R.id.historical_temp_mean);
            precipTv = itemView.findViewById(R.id.historical_precip);
            windTv = itemView.findViewById(R.id.historical_wind);
            humidityTv = itemView.findViewById(R.id.historical_humidity);
        }
    }
}
