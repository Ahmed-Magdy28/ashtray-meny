import 'package:ashtray_meny/screens/wait_screen.dart';
import 'package:flutter/material.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  bool isLoading = true;

  isLoaded() async {
    await Future.delayed(const Duration(seconds: 3));
    Navigator.pushReplacement(context,
        MaterialPageRoute(builder: (context) => const WaitingScreen()));
  }

  @override
  initState() {
    super.initState();
    isLoaded();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        color: Colors.blueGrey,
        child: Center(
          child: SizedBox(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Image.asset('assets/images/Icon.png', width: 200, height: 200),
                const SizedBox(height: 20),
                const CircularProgressIndicator()
              ],
            ),
          ),
        ),
      ),
    );
  }
}
