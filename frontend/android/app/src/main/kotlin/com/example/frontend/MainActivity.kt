package com.example.frontend

import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.telephony.SmsManager
import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val CHANNEL = "smssender-kishea"

    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            if (call.method == "sendSMS") {
                val message = call.argument<String>("message")
                val phoneNumber = call.argument<String>("phoneNumber")
                sendSMS(message, phoneNumber, result)
            } else {
                result.notImplemented()
            }
        }
    }

    private fun sendSMS(message: String?, phoneNumber: String?, result: MethodChannel.Result) {
        if (hasSmsPermission()) {
            try {
                val smsManager = SmsManager.getDefault()
                smsManager.sendTextMessage(phoneNumber, null, message, null, null)
                result.success(true)
            } catch (e: Exception) {
                e.printStackTrace()
                result.success(false)
            }
        } else {
            result.success(false)
        }
    }

    private fun hasSmsPermission(): Boolean {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.SEND_SMS) == PackageManager.PERMISSION_GRANTED) {
                return true
            } else {
                requestPermissions(arrayOf(Manifest.permission.SEND_SMS), 1)
                return false
            }
        } else {
            return true
        }
    }
}
