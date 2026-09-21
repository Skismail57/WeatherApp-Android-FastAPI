package com.Ismail.weatherapp.model;

public class DailyWeather {
    public String dayName;
    public String minTemp;
    public String maxTemp;
    public String pressure;
    public String windSpeed;
    public String humidity;
    public int condition;
    public long sunrise;
    public long sunset;
    public long updateTime;

    public DailyWeather(String dayName, String minTemp, String maxTemp, String pressure, 
                       String windSpeed, String humidity, int condition, long sunrise, 
                       long sunset, long updateTime) {
        this.dayName = dayName;
        this.minTemp = minTemp;
        this.maxTemp = maxTemp;
        this.pressure = pressure;
        this.windSpeed = windSpeed;
        this.humidity = humidity;
        this.condition = condition;
        this.sunrise = sunrise;
        this.sunset = sunset;
        this.updateTime = updateTime;
    }
}
