import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class UserProvider extends ChangeNotifier {
  // User data fields
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

  // Shop data fields (from user_shop relation)
  String? shopId; // ID of the shop associated with the user
  String? shopName;
  String? shopImage;
  String? shopBackgroundImage;
  int? shopViews;
  bool? shopReviewsOn;
  int? shopMonthlySoldItems;
  String? shopSalesThisMonth;
  DateTime? shopCreatedAt;
  String? shopAbout;
  bool? isShopVerified;
  bool? isShopActive;
  List<dynamic>? shopCategories;
  List<dynamic>? shopBestSellers;

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

  // Function to update user and shop data in the provider
  Future<void> getUserData({required Map<String, dynamic> dataSnapShot}) async {
    try {
      userToken = dataSnapShot['token'] ?? "";
      userId = dataSnapShot['user_id'] ?? "";
      userName = dataSnapShot['username'] ?? "";
      userEmail = dataSnapShot['email'] ?? "";
      userImage = dataSnapShot['user_image'] ?? "";
      userAge = dataSnapShot['user_age'] ?? 0;
      aboutUser = dataSnapShot['about_user'] ?? "";
      userCountry = dataSnapShot['user_country'] ?? ""; // Update user country
      isVerified = dataSnapShot['is_verified'] ?? false;
      isStaff = dataSnapShot['is_staff'] ?? false;
      isShopOwner = dataSnapShot['shop_owner'] ?? false;
      ordersCompleted = dataSnapShot['orders_completed'] ?? 0;
      ordersNow = dataSnapShot['orders_now'] ?? 0;

      // Check if the user has a shop and update provider with the shop details
      if (dataSnapShot.containsKey('user_shop') && dataSnapShot['user_shop'] != null) {
        updateShopData(dataSnapShot['user_shop']);
      } else {
        clearShopData(); // Clear the shop data if no shop is found
      }

      // Store token in SharedPreferences
      if (prefs != null) {
        await prefs!.setString('auth_token', userToken);
        await prefs!.setString('user_id', userId);
      }

      notifyListeners(); // Notify listeners to update the UI
    } catch (e) {
      logger.e("Error in getUserData: $e");
    }
  }

  // Function to fetch user data from API
  Future<void> fetchCompleteUserData(String userId, String token) async {
    try {
      final response = await dio.get(
        'http://10.0.2.2:7128/api/users/$userId',
        options: Options(headers: {
          'Authorization': 'Bearer $token',
        }),
      );

      if (response.statusCode == 200) {
        final userData = response.data;
        updateUserFromResponse(userData);
      } else {
        logger.e('Failed to fetch user data. Status code: ${response.statusCode}');
      }
    } catch (e) {
      logger.e('Error fetching user data: $e');
    }
  }

  // Method to update user data from API response or login response
  void updateUserFromResponse(Map<String, dynamic> userData) {
    userName = userData["username"] ?? "";
    userEmail = userData["email"] ?? "";
    userImage = userData["user_image"] ?? "";
    userAge = userData["user_age"] ?? 0;
    aboutUser = userData["about_user"] ?? "";
    userCountry = userData["user_country"] ?? "";
    isVerified = userData["is_verified"] ?? false;
    isStaff = userData["is_staff"] ?? false;
    isShopOwner = userData["shop_owner"] ?? false;
    defaultAddress = userData["default_address"] ?? "";
    ordersCompleted = userData["orders_completed"] ?? 0;
    ordersNow = userData["orders_now"] ?? 0;

    // Update userShopId with the shop ID, if available
    shopId = userData['user_shop'] ?? null;

    // Check if the user has a shop and update shop data
    if (userData.containsKey('user_shop') && userData['user_shop'] != null) {
      updateShopData(userData['user_shop']);
    } else {
      clearShopData();
    }

    notifyListeners(); // Notify listeners so UI can rebuild
  }

  // Update shop-related data from shop creation response or user response
  void updateShopData(Map<String, dynamic> shopData) {
    shopId = shopData['unique_id'];
    shopName = shopData['shop_name'];
    shopImage = shopData['shop_image'];
    shopBackgroundImage = shopData['shop_background_image'];
    shopViews = shopData['shop_views'];
    shopReviewsOn = shopData['shop_reviews_is_on'];
    shopMonthlySoldItems = shopData['monthly_sold_items'];
    shopSalesThisMonth = shopData['shop_sales_this_month'];
    shopCreatedAt = DateTime.parse(shopData['shop_created_at']);
    shopAbout = shopData['shop_about'];
    isShopVerified = shopData['is_verified'];
    isShopActive = shopData['is_active'];
    shopCategories = shopData['category'];
    shopBestSellers = shopData['best_sellers'];

    // Notify listeners to update the UI
    notifyListeners();
  }

  // Clear shop-related data if no shop exists
  void clearShopData() {
    shopId = null;
    shopName = null;
    shopImage = null;
    shopBackgroundImage = null;
    shopViews = null;
    shopReviewsOn = null;
    shopMonthlySoldItems = null;
    shopSalesThisMonth = null;
    shopCreatedAt = null;
    shopAbout = null;
    isShopVerified = null;
    isShopActive = null;
    shopCategories = null;
    shopBestSellers = null;

    notifyListeners(); // Notify listeners to update the UI
  }

  // Reset all user data on logout
  void resetUserData() {
    userName = "";
    userToken = "";
    userEmail = "";
    userId = "";
    userCountry = "";
    userImage = "";
    userAge = 0;
    aboutUser = "";
    isVerified = false;
    isStaff = false;
    isShopOwner = false;
    defaultAddress = "";
    ordersCompleted = 0;
    ordersNow = 0;

    // Clear shop data
    clearShopData();

    notifyListeners(); // Notify listeners to update the UI
  }

  // Function to save the user with a shop ID (e.g., after shop creation)
  static Future<void> saveTheShopUser({required BuildContext context}) async {
    try {
      final response = await dio.patch(
        'http://10.0.2.2:7128/api/users/$userId/',
        data: {
          'user_shop': userShop, // Save the shop ID in the user's profile
        },
        options: Options(headers: {
          'Authorization': 'Bearer $userToken',
        }),
      );

      if (response.statusCode == 200) {
        // Successfully updated user_shop, update the provider with the new user data
        updateUserFromResponse(response.data);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Shop linked to user successfully')),
        );
      } else {
        throw Exception('Failed to save the shop for the user');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }
}
