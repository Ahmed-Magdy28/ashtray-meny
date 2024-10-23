import 'package:ashtray_meny/classes/routes.dart';
import 'package:ashtray_meny/widgets/navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class CartScreen extends StatefulWidget {
  const CartScreen({super.key});

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  List<dynamic> cart = [];

  @override
  void initState() {
    super.initState();
    _loadCart();
  }

  Future<void> _loadCart() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    String? cartItems = prefs.getString('cart');
    setState(() {
      cart = cartItems != null ? json.decode(cartItems) : [];
    });
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        Routes.navigateToMainAndClearStack(context: context);
        return false;
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Cart'),
        ),
        body: cart.isEmpty
            ? const Center(child: Text('Your cart is empty'))
            : ListView.builder(
                itemCount: cart.length,
                itemBuilder: (context, index) {
                  final product = cart[index];
                  return Card(
                    child: ListTile(
                      leading: Image.network(product['image_1'], width: 50),
                      title: Text(product['product_name']),
                      subtitle: Text("\$${product['price']}"),
                      trailing: IconButton(
                        icon: const Icon(Icons.remove_circle_outline),
                        onPressed: () {
                          _removeFromCart(index);
                        },
                      ),
                    ),
                  );
                },
              ),
        bottomNavigationBar: const MyNavigationBar(
          initialIndex: 2,
        ),
      ),
    );
  }

  Future<void> _removeFromCart(int index) async {
    setState(() {
      cart.removeAt(index);
    });

    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('cart', json.encode(cart));

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Product removed from cart')),
    );
  }
}
