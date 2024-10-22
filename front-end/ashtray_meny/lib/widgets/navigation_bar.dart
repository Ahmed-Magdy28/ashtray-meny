import 'package:ashtray_meny/classes/routes.dart';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';

class MyNavigationBar extends StatefulWidget {
  final int initialIndex; // Pass the initial index to highlight the correct tab

  const MyNavigationBar(
      {super.key, this.initialIndex = 0}); // Default index is 0 (Home)

  @override
  State<MyNavigationBar> createState() => _MyNavigationBarState();
}

class _MyNavigationBarState extends State<MyNavigationBar> {
  late int _selectedIndex; // Track the selected tab
  Logger logger = Logger();

  @override
  void initState() {
    super.initState();
    _selectedIndex =
        widget.initialIndex; // Set the initial tab based on passed index
  }

  // Function to handle navigation tab selection and perform actions
  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index; // Update selected index
    });

    // Perform navigation based on the selected tab
    switch (index) {
      case 0:
        logger.d('Home tab clicked');
        Routes.navigateToMainAndClearStack (
            context: context); // You can update the route here
        break;
      case 1:
        logger.d('Profile tab clicked');
        Routes.profileRoute(context: context); // Navigate to profile screen
        break;
      case 2:
        logger.d('Cart tab clicked');
        Routes.toCartScreen(context: context); // Navigate to cart screen
        break;
      case 3:
        logger.d('Menu tab clicked');
        Routes.toMenuScreen(context: context); // Navigate to menu screen
        break;
      default:
        logger.d('Unknown tab clicked');
    }
  }

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      currentIndex: _selectedIndex, // Set the selected tab index
      onTap: _onItemTapped, // Handle tab selection

      // Bottom Navigation Bar items
      items: const <BottomNavigationBarItem>[
        BottomNavigationBarItem(
          icon: Icon(Icons.home),
          label: 'Home',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.person),
          label: 'Profile',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.shopping_cart),
          label: 'Cart',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.menu),
          label: 'Menu',
        ),
      ],

      // Styling the navigation bar
      selectedItemColor: Colors.black, // Black color for the selected item
      unselectedItemColor: Colors.black54, // Lighter black for unselected items
      showUnselectedLabels: true, // Show labels for unselected items
      type: BottomNavigationBarType
          .fixed, // Fixes the icons and labels to the bottom
      backgroundColor:
          Colors.white, // Ensure the background is white (for light mode)
      elevation: 10, // Add slight elevation for a polished look
    );
  }
}
