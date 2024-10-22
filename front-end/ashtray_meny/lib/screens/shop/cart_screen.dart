import 'package:ashtray_meny/widgets/navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:ashtray_meny/classes/routes.dart';

class CartScreen extends StatelessWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        // Return to MainScreen instead of going back step by step
        Routes.navigateToMainAndClearStack(context: context);
        return false;
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Cart'),
        ),
        body: const Center(
          child: Text('This is the Cart Screen'),
        ),
        bottomNavigationBar: const MyNavigationBar(
          initialIndex: 2,
        ),
      ),
    );
  }
}
