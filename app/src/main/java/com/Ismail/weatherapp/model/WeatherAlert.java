package com.Ismail.weatherapp.model;

public class WeatherAlert {
    public String id;
    public String title;
    public String description;
    public String severity;
    public String area;
    public long effectiveTime;
    public long expiresTime;
    public String source;
    public String sourceUrl;

    public WeatherAlert(String id, String title, String description, String severity, String area,
                       long effectiveTime, long expiresTime, String source, String sourceUrl) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.severity = severity;
        this.area = area;
        this.effectiveTime = effectiveTime;
        this.expiresTime = expiresTime;
        this.source = source;
        this.sourceUrl = sourceUrl;
    }
}
