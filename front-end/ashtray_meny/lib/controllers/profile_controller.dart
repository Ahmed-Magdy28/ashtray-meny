import 'package:ashtray_meny/classes/routes.dart';
import 'package:ashtray_meny/providers/user_provider.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ProfileController {
  // Function to turn the user into a shop owner by sending a request to the server

  static Future<void> turnToShopOwner({required BuildContext context}) async {
    final userProvider = Provider.of<UserProvider>(context, listen: false);

    try {
      // Make the API call to update the user status
      final response = await Dio().patch(
        'http://10.0.2.2:7128/api/users/${userProvider.userId}/',
        data: {
          'shop_owner': true,
        },
        options: Options(headers: {
          'Authorization':
              'Bearer ${userProvider.userToken}', // Use the token for authorization
        }),
      );

      if (response.statusCode == 200) {
        // Update the provider with the new user data from the response
        userProvider.updateUserFromResponse(response.data);

        // Show success message
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('You are now a Shop Owner!')),
        );
      } else {
        throw Exception('Failed to update user status');
      }
    } catch (e) {
      // Handle the error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  // Navigate to the user's shop (placeholder function, implement accordingly)
  static void goToUserShop({required BuildContext context}) {
    // You can define the route to the user's shop here
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Navigating to your shop...')),
    );
    Routes.toUserShop(context: context);
  }
}
