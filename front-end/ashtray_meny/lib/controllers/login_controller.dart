import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';

class LoginController {
  // Single Dio instance
  static final dio = Dio();

  // Logger instance
  static var logger = Logger();

  static Future<Map<String, String>?> login(
      {required String email, required String password}) async {
    Map<String, String> data = {
      "email": email,
      "password": password,
    };
    try {
      // Send POST request
      Response response = await dio.post(
        'http://10.0.2.2:7128/api/user/login/',
        data: {
          'email': email,
          'password': password,
        },
      );

      // Check the status code or the response body as needed
      if (response.statusCode == 200) {
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
}
