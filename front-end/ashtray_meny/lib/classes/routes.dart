import 'package:flutter/material.dart';
import 'package:ashtray_meny/screens/Login/forget_password_screen.dart';
import 'package:ashtray_meny/screens/Login/login_screen.dart';
import 'package:ashtray_meny/screens/Login/sign_up_screen.dart';
import 'package:ashtray_meny/screens/main_screen.dart';
import 'package:ashtray_meny/screens/profile/edit_profile_screen.dart';
import 'package:ashtray_meny/screens/profile/profile_screen.dart';
import 'package:ashtray_meny/screens/settings/menu_screen.dart';
import 'package:ashtray_meny/screens/settings/settings_screen.dart';
import 'package:ashtray_meny/screens/shop/cart_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';

class Routes {
  // Fade transition animation (default)
  static PageRouteBuilder _createFadeRoute(Widget page) {
    return PageRouteBuilder(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = 0.0;
        const end = 1.0;
        const curve = Curves.easeInOut;

        var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

        return FadeTransition(
          opacity: animation.drive(tween),
          child: child,
        );
      },
    );
  }

  // Always navigate to MainScreen and clear previous routes
  static void navigateToMainAndClearStack({required BuildContext context}) {
    Navigator.of(context).pushAndRemoveUntil(
      _createFadeRoute(const MainScreen()),
      (route) => false,
    );
  }

  // Forget password route
  static void forgetPassword({required BuildContext context}) {
    Navigator.of(context).push(_createFadeRoute(const ForgetPasswordScreen()));
  }

  // Sign Up route
  static void openSignUp({required BuildContext context}) {
    Navigator.of(context).push(_createFadeRoute(const SignUpScreen()));
  }

  // Login route
  static void openLogin({required BuildContext context}) {
    Navigator.of(context).push(_createFadeRoute(const LoginScreen()));
  }

  // Navigate to Profile Screen but return directly to MainScreen when pressing back
  static void profileRoute({required BuildContext context}) {
    Navigator.of(context).push(_createFadeRoute(const ProfileScreen()));
  }

  // Navigate to Settings
  static void settingRoute({required BuildContext context}) {
    Navigator.of(context).push(_createFadeRoute(const SettingsScreen()));
  }

  // Edit Profile route
  static void toEditProfile({required BuildContext context}) {
    Navigator.of(context).push(_createFadeRoute(const EditProfileScreen()));
  }

  // Navigate to Cart Screen but return to MainScreen when pressing back
  static void toCartScreen({required BuildContext context}) {
    Navigator.of(context).push(_createFadeRoute(const CartScreen()));
  }

  // Navigate to Menu Screen but return to MainScreen when pressing back
  static void toMenuScreen({required BuildContext context}) {
    Navigator.of(context).push(_createFadeRoute(const MenuScreen()));
  }

  // Logout method - clears session and navigates to Login
  static Future<void> logout({required BuildContext context}) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
    await prefs.remove('user_id');

    Navigator.of(context).pushReplacement(_createFadeRoute(const LoginScreen()));
  }
}
