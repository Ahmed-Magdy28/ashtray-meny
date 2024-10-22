import 'package:ashtray_meny/widgets/navigation_bar.dart';
import 'package:flutter/material.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: Text("mainScreen"),
      ),
      bottomNavigationBar: MyNavigationBar(
        initialIndex: 0,
      ),
    );
  }
}
