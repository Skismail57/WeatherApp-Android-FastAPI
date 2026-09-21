package com.Ismail.weatherapp.utils;

import android.util.Log;

import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.TextStyle;
import java.util.Locale;
import java.util.TimeZone;

public class TimeUtils {
    private static final String TAG = "TimeUtils";

    /**
     * Get formatted local time string for a timezone
     * Format: "10:30 PM · IST · UTC+05:30"
     */
    public static String getFormattedLocalTime(String timezoneId, int timezoneOffsetSeconds) {
        if (timezoneId == null || timezoneId.isEmpty()) {
            Log.e(TAG, "DEBUG - getFormattedLocalTime: timezoneId is null or empty");
            return "";
        }

        try {
            ZoneId zoneId = ZoneId.of(timezoneId);
            ZonedDateTime now = ZonedDateTime.now(zoneId);
            
            Log.d(TAG, "DEBUG - getFormattedLocalTime - timezoneId: " + timezoneId + ", ZoneId created: " + zoneId + ", ZonedDateTime.now(zoneId): " + now);
            
            // Format time as "10:30 PM"
            DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("h:mm a", Locale.ENGLISH);
            String timeStr = now.format(timeFormatter);
            
            // Format UTC offset as "UTC+05:30" or "UTC-05:00"
            String utcOffset = formatUTCOffset(timezoneOffsetSeconds);
            
            String result = String.format("%s · %s", timeStr, utcOffset);
            Log.d(TAG, "DEBUG - getFormattedLocalTime - timeStr: " + timeStr + ", utcOffset: " + utcOffset + ", result: " + result);
            return result;
        } catch (Exception e) {
            Log.e(TAG, "DEBUG - getFormattedLocalTime ERROR: " + e.getMessage());
            return "";
        }
    }

    /**
     * Get timezone abbreviation using multiple approaches
     */
    private static String getTimezoneAbbreviation(ZoneId zoneId, ZonedDateTime now) {
        // Try using DateTimeFormatter with 'z' pattern on ZonedDateTime (DST-aware)
        try {
            DateTimeFormatter tzFormatter = DateTimeFormatter.ofPattern("z", Locale.ENGLISH);
            String abbrev = now.format(tzFormatter);
            Log.d(TAG, "DEBUG - getTimezoneAbbreviation - DateTimeFormatter approach: " + abbrev);
            return abbrev;
        } catch (Exception e) {
            Log.e(TAG, "DEBUG - getTimezoneAbbreviation - DateTimeFormatter approach failed: " + e.getMessage());
        }
        
        // Fallback to java.util.TimeZone with DST awareness
        try {
            TimeZone tz = TimeZone.getTimeZone(zoneId);
            boolean isDST = tz.inDaylightTime(java.util.Date.from(now.toInstant()));
            String abbrev = tz.getDisplayName(isDST, TimeZone.SHORT, Locale.ENGLISH);
            Log.d(TAG, "DEBUG - getTimezoneAbbreviation - TimeZone approach: " + abbrev);
            return abbrev;
        } catch (Exception e) {
            Log.e(TAG, "DEBUG - getTimezoneAbbreviation - TimeZone approach failed: " + e.getMessage());
        }
        
        // Ultimate fallback to timezone ID
        return zoneId.getId();
    }

    /**
     * Get day period based on local time using fixed time ranges
     * Returns: "Morning", "Afternoon", "Evening", or "Night"
     * 
     * Fixed local-time ranges:
     * Morning: 05:00 AM through 11:59 AM
     * Afternoon: 12:00 PM through 04:59 PM
     * Evening: 05:00 PM through 08:59 PM
     * Night: 09:00 PM through 04:59 AM
     */
    public static String getDayPeriod(String timezoneId, long sunriseUnix, long sunsetUnix) {
        if (timezoneId == null || timezoneId.isEmpty()) {
            Log.e(TAG, "DEBUG - getDayPeriod: timezoneId is null or empty, using fallback");
            return getDayPeriodFromTimeOnly();
        }

        try {
            ZoneId zoneId = ZoneId.of(timezoneId);
            ZonedDateTime now = ZonedDateTime.now(zoneId);
            int currentHour = now.getHour();
            
            Log.d(TAG, "DEBUG - getDayPeriod - timezoneId: " + timezoneId + ", ZoneId: " + zoneId + ", Current local time: " + now + ", Hour: " + currentHour);
            
            // Use fixed local-time ranges for day period
            String period = getDayPeriodFromHour(currentHour);
            Log.d(TAG, "DEBUG - getDayPeriod - Result: " + period + " (fixed time range)");
            return period;
        } catch (Exception e) {
            Log.e(TAG, "DEBUG - getDayPeriod ERROR: " + e.getMessage());
            return getDayPeriodFromTimeOnly();
        }
    }

    /**
     * Get day period icon based on period
     * Returns emoji: 🌙, 🌅, ☀️, 🌇
     */
    public static String getDayPeriodIcon(String dayPeriod) {
        if (dayPeriod == null) {
            return "🌙";
        }
        
        switch (dayPeriod.toLowerCase()) {
            case "morning":
                return "🌅";
            case "afternoon":
                return "☀️";
            case "evening":
                return "🌇";
            case "night":
            default:
                return "🌙";
        }
    }

    /**
     * Format UTC offset seconds to "UTC+05:30" or "UTC-05:00"
     */
    private static String formatUTCOffset(int offsetSeconds) {
        int hours = offsetSeconds / 3600;
        int minutes = Math.abs((offsetSeconds % 3600) / 60);
        
        String sign = hours >= 0 ? "+" : "-";
        int absHours = Math.abs(hours);
        
        if (minutes == 0) {
            return String.format("UTC%s%02d:00", sign, absHours);
        } else {
            return String.format("UTC%s%02d:%02d", sign, absHours, minutes);
        }
    }

    /**
     * Get day period from current hour using fixed time ranges
     * 
     * Fixed local-time ranges:
     * Morning: 05:00 AM through 11:59 AM (hours 5-11)
     * Afternoon: 12:00 PM through 04:59 PM (hours 12-16)
     * Evening: 05:00 PM through 08:59 PM (hours 17-20)
     * Night: 09:00 PM through 04:59 AM (hours 21-4)
     */
    private static String getDayPeriodFromHour(int hour) {
        if (hour >= 5 && hour < 12) {
            return "Morning";
        } else if (hour >= 12 && hour < 17) {
            return "Afternoon";
        } else if (hour >= 17 && hour < 21) {
            return "Evening";
        } else {
            return "Night";
        }
    }

    /**
     * Get day period from current device time (ultimate fallback)
     */
    private static String getDayPeriodFromTimeOnly() {
        int hour = ZonedDateTime.now().getHour();
        return getDayPeriodFromHour(hour);
    }
}
