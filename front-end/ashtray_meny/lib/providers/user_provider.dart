import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class UserProvider extends ChangeNotifier {
  // User data fields (instance members)
  String userName = "";
  String userToken = "";
  String userEmail = "";
  String userId = "";
  String userCountry = "";
  String userImage = "";
  int userAge = 0;
  String aboutUser = "";
  bool isVerified = false;
  bool isStaff = false;
  bool isShopOwner = false;
  String defaultAddress = "";
  int ordersCompleted = 0;
  int ordersNow = 0;

  // Logger for debugging
  var logger = Logger();

  // Dio instance to make API requests
  Dio dio = Dio();

  SharedPreferences? prefs;

  // Constructor to initialize SharedPreferences
  UserProvider() {
    _initializePreferences();
  }

  // Initialize SharedPreferences asynchronously
  Future<void> _initializePreferences() async {
    prefs = await SharedPreferences.getInstance();
    // Optionally load the saved user data here
    loadSavedUserData();
  }

  // Load user data from SharedPreferences (if needed)
  void loadSavedUserData() {
    if (prefs != null) {
      userToken = prefs!.getString('auth_token') ?? "";
      userId = prefs!.getString('user_id') ?? "";

      if (userToken.isNotEmpty && userId.isNotEmpty) {
        fetchCompleteUserData(userId, userToken);
      }
    }
  }

  // Function to update user data in the provider
  Future<void> getUserData({required Map<String, dynamic> dataSnapShot}) async {
    try {
      if (dataSnapShot.containsKey('token') &&
          dataSnapShot.containsKey('user_id')) {
        userToken = dataSnapShot['token'] ?? "";
        userId = dataSnapShot['user_id'] ?? "";

        // Optionally store the token in SharedPreferences
        if (prefs != null) {
          await prefs!.setString('auth_token', userToken);
          await prefs!.setString('user_id', userId);
        }

        // You can optionally store the refresh token if needed
        if (dataSnapShot.containsKey('refresh_token')) {
          // Handle refresh token if needed
        }

        if (userToken.isNotEmpty && userId.isNotEmpty) {
          // Fetch all the user data from another API using the user ID and token
          fetchCompleteUserData(userId, userToken);
        }
      }
    } catch (e) {
      logger.e("Error in getUserData: $e");
    }
  }

  // Function to fetch all user data from the API
  Future<void> fetchCompleteUserData(String userId, String token) async {
    try {
      // Example API endpoint, replace with your actual API
      final response = await dio.get(
        'http://10.0.2.2:7128/api/users/$userId',
        options: Options(headers: {
          'Authorization':
              'Bearer $token', // Attach the token for authorization
        }),
      );

      if (response.statusCode == 200) {
        // Assuming the response contains a JSON object with user data
        final userData = response.data;

        // Update provider with the user data
        userName = userData["username"] ?? "";
        userEmail = userData["email"] ?? "";
        userCountry = userData["country"] ?? "";
        userImage = userData["user_image"] ?? "";
        userAge = userData["user_age"] ?? 0;
        aboutUser = userData["about_user"] ?? "";
        isVerified = userData["is_verified"] ?? false;
        isStaff = userData["is_staff"] ?? false;
        isShopOwner = userData["shop_owner"] ?? false;
        defaultAddress = userData["default_address"] ?? "";
        ordersCompleted = userData["orders_completed"] ?? 0;
        ordersNow = userData["orders_now"] ?? 0;

        // Notify listeners to update the UI wherever this provider is used
        notifyListeners();
      } else {
        logger.e(
            'Failed to fetch user data. Status code: ${response.statusCode}');
      }
    } catch (e) {
      logger.e('Error fetching user data: $e');
    }
  }
}
