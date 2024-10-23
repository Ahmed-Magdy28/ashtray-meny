import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';

class SignupController {
  // Single Dio instance
  static final dio = Dio();

  // Logger instance
  static var logger = Logger();

  // Function to create a new user
  static Future<bool> createUser(
      {required BuildContext context,
      required String email,
      required String username,
      required String password,
      required String country}) async {
    Map<String, String> data = {
      "email": email,
      "username": username,
      "password": password,
      "user_country": country,
    };

    try {
      // Make POST request
      Response response = await dio.post(
        'http://10.0.2.2:7128/api/user/create/',
        data: data,
      );

      // Check if the response status code is OK (200-299)
      if (response.statusCode != null &&
          response.statusCode! >= 200 &&
          response.statusCode! < 300) {
        logger.d("Signup successful: ${response.data}");
        _showSnackBar(context, response.data.toString(), Colors.blue[400]!);
        return true;
      } else {
        logger.w("Signup failed: ${response.statusCode} - ${response.data}");
        _showSnackBar(
            context, "Signup failed. Please try again.", Colors.red[400]!);
        return false;
      }
    } on DioException catch (dioError) {
      // DioError for network and server-related issues
      logger.e('Dio error occurred: ${dioError.message}');
      _showSnackBar(
          context,
          "Error: ${dioError.response?.data ?? dioError.message}",
          Colors.red[400]!);
      return false;
    } catch (e) {
      // Any other error
      logger.e('An unexpected error occurred: $e');
      _showSnackBar(context, "An unexpected error occurred.", Colors.red[400]!);
      return false;
    }
  }

  // Helper function to show SnackBar
  static void _showSnackBar(BuildContext context, String message, Color color) {
    final snackBar = SnackBar(
      backgroundColor: color,
      content: Text(message),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }
}
