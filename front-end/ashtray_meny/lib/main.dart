import 'package:ashtray_meny/screens/splash_screen.dart';
import 'package:flutter/material.dart';


void main() {
  runApp(const AshtaryMeny());
}

class AshtaryMeny extends StatefulWidget {
  const AshtaryMeny({super.key});

  @override
  State<AshtaryMeny> createState() => _AshtaryMenyState();
}

class _AshtaryMenyState extends State<AshtaryMeny> {
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'AshtaryMeny',
      home: SplashScreen(),
    );
  }
}
