import 'package:ashtray_meny/classes/routes.dart';
import 'package:ashtray_meny/widgets/navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class MenuScreen extends StatefulWidget {
  const MenuScreen({super.key});

  @override
  State<MenuScreen> createState() => _MenuScreenState();
}

class _MenuScreenState extends State<MenuScreen> {
  // Sample list of menu options
  final List<Map<String, dynamic>> _menuItems = [
    {'title': 'Profile', 'icon': Icons.person, 'route': Routes.profileRoute},
    {'title': 'Settings', 'icon': Icons.settings, 'route': Routes.settingRoute},
    {
      'title': 'Cart',
      'icon': Icons.shopping_cart,
      'route': Routes.toCartScreen
    },
    // You can add more options here
  ];

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        // Return to MainScreen instead of going back step by step
        Routes.navigateToMainAndClearStack(context: context);
        return false; // Prevent the default back button behavior
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Menu'),
        ),
        body: ListView.builder(
          itemCount: _menuItems.length + 1, // Add 1 for the logout button
          itemBuilder: (context, index) {
            if (index == _menuItems.length) {
              // Last tile is the logout option
              return ListTile(
                leading: const Icon(Icons.logout, color: Colors.red),
                title: const Text('Logout'),
                onTap: () async {
                  await Routes.logout(context: context);
                },
              );
            }
            // Build the other menu options
            return ListTile(
              leading: Icon(_menuItems[index]['icon']),
              title: Text(_menuItems[index]['title']),
              onTap: () {
                _menuItems[index]['route'](context: context);
              },
            );
          },
        ),
        bottomNavigationBar: const MyNavigationBar(
          initialIndex: 3,
        ),
      ),
    );
  }
}
