import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginController {
  // Single Dio instance
  static final dio = Dio();

  // Logger instance
  static var logger = Logger();

  static Future<Map<String, dynamic>?> login(
      {required String email, required String password}) async {
    Map<String, dynamic> data = {
      "email": email,
      "password": password,
    };
    try {
      // Send POST request
      Response response = await dio.post(
        'http://10.0.2.2:7128/api/user/login/',
        data: data,
      );

      // Check the status code or the response body as needed
      if (response.statusCode == 200) {
        // Get the token and user_id
        final token = response.data['token'];
        final userId = response.data['user_id'];

        // Save the token in SharedPreferences
        SharedPreferences prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', token);
        await prefs.setString('user_id', userId);

        return response
            .data; // Assume the response data is a Map<String, dynamic>
      } else {
        logger.e(response.statusCode);
        return null;
      }
    } catch (e) {
      logger.e(e);
      return null;
    }
  }

  // Load saved email and password from SharedPreferences
  static Future<Map<String, dynamic>?> loadUserCredentials() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? savedEmail = prefs.getString('saved_email');
    String? savedPassword = prefs.getString('saved_password');
    bool? savedRememberMe = prefs.getBool('remember_me');

    return {
      'email': savedEmail,
      'password': savedPassword,
      'rememberMe': savedRememberMe,
    };
  }

  // Save email and password in SharedPreferences
  static Future<void> saveUserCredentials({
    required bool rememberMe,
    required String email,
    required String password,
  }) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();

    if (rememberMe) {
      await prefs.setString('saved_email', email);
      await prefs.setString('saved_password', password);
    } else {
      await prefs.remove('saved_email');
      await prefs.remove('saved_password');
    }
    await prefs.setBool('remember_me', rememberMe);
  }
}
