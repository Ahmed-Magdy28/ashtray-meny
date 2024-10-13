import 'package:ashtray_meny/screens/Login/forget_password_screen.dart';
import 'package:ashtray_meny/screens/Login/login_screen.dart';
import 'package:ashtray_meny/screens/Login/sign_up_screen.dart';
import 'package:ashtray_meny/screens/profile/edit_profile_screen.dart';
import 'package:ashtray_meny/screens/profile/profile_screen.dart';
import 'package:ashtray_meny/screens/settings/settings_screen.dart';
import 'package:flutter/material.dart';

class Routes {
  static void forgetPassword({required BuildContext context}) {
    Navigator.push(context,
        MaterialPageRoute(builder: (context) => const ForgetPasswordScreen()));
  }

  static void openSignUp({required BuildContext context}) {
    Navigator.push(
        context, MaterialPageRoute(builder: (context) => const SignUpScreen()));
  }

  static void openLogin({required BuildContext context}) {
    Navigator.push(
        context, MaterialPageRoute(builder: (context) => const LoginScreen()));
  }

  static void loginMaster({required BuildContext context}) {
    Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => const LoginScreen()),
        (route) => false);
  }

  static void profileRoute({required BuildContext context}) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const ProfileScreen(),
      ),
    );
  }

  static void settingRoute({required BuildContext context}) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const SettingsScreen(),
      ),
    );
  }

  static void toEditProfile({required BuildContext context}) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const EditProfileScreen(),
      ),
    );
  }
}
