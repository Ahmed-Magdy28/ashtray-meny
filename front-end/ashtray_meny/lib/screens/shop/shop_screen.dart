import 'package:ashtray_meny/classes/routes.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ashtray_meny/providers/user_provider.dart';
import 'package:ashtray_meny/widgets/navigation_bar.dart';

class ShopScreen extends StatefulWidget {
  const ShopScreen({super.key});

  @override
  State<ShopScreen> createState() => _ShopScreenState();
}

class _ShopScreenState extends State<ShopScreen> {
  bool isLoading = false;

  Future<void> _refreshShopData() async {
    setState(() {
      isLoading = true;
    });

    // Simulate fetching new data from the API or provider
    final userProvider = Provider.of<UserProvider>(context, listen: false);

    // Fetch updated shop data
    await userProvider.fetchCompleteUserData(
        userProvider.userId, userProvider.userToken);

    setState(() {
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);
    final products = userProvider.shopCategories ??
        []; // Assuming shopCategories is a product list

    return Scaffold(
      appBar: AppBar(
        title: Text(userProvider.shopName ?? "Your Shop"),
        centerTitle: true,
      ),
      body: RefreshIndicator(
        onRefresh: _refreshShopData,
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Shop Details Section
              _buildShopDetails(userProvider),

              const SizedBox(height: 20),

              // Products Grid Section
              products.isEmpty
                  ? _buildNoProductsView()
                  : _buildProductGrid(products),
            ],
          ),
        ),
      ),
      bottomNavigationBar: const MyNavigationBar(),
    );
  }

  // Shop Details UI
  Widget _buildShopDetails(UserProvider userProvider) {
    return Column(
      children: [
        if (userProvider.shopImage != null)
          Image.network(
            userProvider.shopImage!,
            height: 200,
            width: double.infinity,
            fit: BoxFit.cover,
          ),
        const SizedBox(height: 16),
        Text(
          userProvider.shopName ?? "Shop Name",
          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        Text(
          userProvider.shopAbout ?? "No description provided",
          style: const TextStyle(fontSize: 16, color: Colors.grey),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 16),
        Text(
          "Products: ${userProvider.shopMonthlySoldItems ?? 0}",
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
        ),
        const SizedBox(height: 16),
      ],
    );
  }

  // Build Grid of Products
  Widget _buildProductGrid(List<dynamic> products) {
    return GridView.builder(
      padding: const EdgeInsets.all(8.0),
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: products.length,
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2, // Two items per row
        crossAxisSpacing: 8.0,
        mainAxisSpacing: 8.0,
        childAspectRatio: 3 / 4,
      ),
      itemBuilder: (context, index) {
        final product = products[index];
        return _buildProductTile(product);
      },
    );
  }

  // Build No Products View
  Widget _buildNoProductsView() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text(
            "No products available.",
            style: TextStyle(fontSize: 18, color: Colors.grey),
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () {
              Routes.toAddProductScreen(context: context);
            }, // Implement product addition
            child: const Text("Add First Product"),
          ),
        ],
      ),
    );
  }

  // Product Tile UI
  Widget _buildProductTile(dynamic product) {
    return Card(
      elevation: 2,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Product Image
          if (product['image_url'] != null)
            Image.network(
              product['image_url'],
              height: 120,
              fit: BoxFit.cover,
            ),
          const SizedBox(height: 8),
          // Product Name
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: Text(
              product['name'] ?? "Product Name",
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          const SizedBox(height: 4),
          // Product Price
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: Text(
              "\$${product['price']}",
              style: const TextStyle(fontSize: 14, color: Colors.green),
            ),
          ),
        ],
      ),
    );
  }
}
