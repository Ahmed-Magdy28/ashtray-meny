import 'package:ashtray_meny/providers/user_provider.dart';
import 'package:ashtray_meny/screens/Login/login_screen.dart';
import 'package:ashtray_meny/screens/main_screen.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:provider/provider.dart';
import 'package:ashtray_meny/controllers/login_controller.dart'; // Import LoginController

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => UserProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool isLoggedIn = false;

  @override
  void initState() {
    super.initState();
    _checkLoginStatus();
  }

  // Check if the token exists and redirect appropriately
  Future<void> _checkLoginStatus() async {
    bool loggedIn = await LoginController.isLoggedIn();

    if (loggedIn) {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      String? token = prefs.getString('auth_token');
      String? userId = prefs.getString('user_id');

      if (token != null && userId != null) {
        // Fetch user data and auto-login
        final userProvider = Provider.of<UserProvider>(context, listen: false);
        userProvider.getUserData(dataSnapShot: {
          'token': token,
          'user_id': userId,
        });
        setState(() {
          isLoggedIn = true;
        });
      }
    } else {
      // No token, direct to login screen
      setState(() {
        isLoggedIn = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: isLoggedIn
          ? const MainScreen() // Show HomeScreen if logged in
          : const LoginScreen(), // Show LoginScreen if not logged in
    );
  }
}
