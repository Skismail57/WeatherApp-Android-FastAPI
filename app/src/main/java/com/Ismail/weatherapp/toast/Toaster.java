package com.Ismail.weatherapp.toast;

import android.content.Context;
import android.widget.Toast;

public class Toaster {

    public static void successToast(Context context, String msg) {
        Toast.makeText(context, msg, Toast.LENGTH_SHORT).show();
    }

    public static void errorToast(Context context, String msg) {
        Toast.makeText(context, msg, Toast.LENGTH_SHORT).show();
    }
}