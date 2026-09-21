package com.Ismail.weatherapp.model;

public class HourlyWeather {
    public long time;
    public int timezoneOffset;
    public String temperature;
    public String weatherDescription;
    public String weatherIcon;
    public String precipitationProbability;

    public HourlyWeather(long time, int timezoneOffset, String temperature, String weatherDescription, 
                         String weatherIcon, String precipitationProbability) {
        this.time = time;
        this.timezoneOffset = timezoneOffset;
        this.temperature = temperature;
        this.weatherDescription = weatherDescription;
        this.weatherIcon = weatherIcon;
        this.precipitationProbability = precipitationProbability;
    }
}
