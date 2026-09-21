package com.Ismail.weatherapp.model;

public class HistoricalWeatherData {
    public String date;
    public double temperatureMax;
    public double temperatureMin;
    public double temperatureMean;
    public double precipitationSum;
    public double precipitationHours;
    public double windSpeedMax;
    public double humidityMean;

    public HistoricalWeatherData(String date, double temperatureMax, double temperatureMin, double temperatureMean,
                                double precipitationSum, double precipitationHours, double windSpeedMax, double humidityMean) {
        this.date = date;
        this.temperatureMax = temperatureMax;
        this.temperatureMin = temperatureMin;
        this.temperatureMean = temperatureMean;
        this.precipitationSum = precipitationSum;
        this.precipitationHours = precipitationHours;
        this.windSpeedMax = windSpeedMax;
        this.humidityMean = humidityMean;
    }
}
