import 'package:ashtray_meny/classes/routes.dart';
import 'package:ashtray_meny/providers/user_provider.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import 'package:provider/provider.dart';

class CreateUserShopScreen extends StatefulWidget {
  const CreateUserShopScreen({super.key});

  @override
  State<CreateUserShopScreen> createState() => _CreateUserShopScreenState();
}

class _CreateUserShopScreenState extends State<CreateUserShopScreen> {
  final _shopNameController = TextEditingController(); // For shop name input
  bool isLoading =
      false; // For showing loading indicator while the shop is being created
  var logger = Logger();
  @override
  void dispose() {
    _shopNameController.dispose();
    super.dispose();
  }

  Future<void> _createShop() async {
    final userProvider = Provider.of<UserProvider>(context, listen: false);
    final String shopName = _shopNameController.text.trim();

    if (shopName.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter a shop name')),
      );
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      final response = await Dio().post(
        'http://10.0.2.2:7128/api/shops/',
        data: {
          'shop_name': shopName,
          'shop_owner': userProvider.userId, // User ID from provider
        },
        options: Options(headers: {
          'Authorization':
              'Bearer ${userProvider.userToken}', // Token from provider
        }),
      );

      if (response.statusCode == 201) {
        final shopData = response.data;

        // Update the UserProvider with the new shop data
        userProvider.updateShopData(shopData);

        // Update the user_shop field in UserProvider with the new shop ID
        userProvider.updateUserShop(shopData['unique_id']);
        userProvider.saveTheShopUser(
            context: context); // Save the shop ID to the user

        // Navigate to the shop screen
        Routes.toUserShop(context: context); // Implement the ShopScreen route
      } else {
        logger.e('Failed to create shop: ${response.data}');
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to create shop')),
        );
      }
    } catch (e) {
      logger.e(e);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Shop'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Enter your shop details',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _shopNameController,
              decoration: const InputDecoration(
                labelText: 'Shop Name',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: isLoading
                    ? null
                    : _createShop, // Disable button while loading
                child: isLoading
                    ? const CircularProgressIndicator(
                        color: Colors.white,
                      )
                    : const Text('Create Shop'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
