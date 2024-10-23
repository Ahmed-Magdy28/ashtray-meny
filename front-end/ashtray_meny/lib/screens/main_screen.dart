import 'package:ashtray_meny/widgets/navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:logger/logger.dart';
import 'package:provider/provider.dart';
import 'package:ashtray_meny/providers/user_provider.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<dynamic> categories = [];
  List<dynamic> products = [];
  bool isLoadingCategories = true;
  bool isLoadingProducts = true;
  var logger = Logger();

  @override
  void initState() {
    super.initState();
    _fetchCategories();
    _fetchProducts();
  }

  Future<void> _fetchCategories() async {
    try {
      final userProvider = Provider.of<UserProvider>(context, listen: false);
      final response = await Dio().get(
        'http://10.0.2.2:7128/api/categories/',
        options: Options(headers: {
          'Authorization': 'Bearer ${userProvider.userToken}',
        }),
      );

      if (response.statusCode == 200) {
        setState(() {
          categories = response.data;
          isLoadingCategories = false;
        });
      } else {
        logger.e('Failed to load categories');
        _showError('Failed to load categories');
      }
    } catch (e) {
      logger.e('Failed to load categories');
      _showError('Error loading categories: $e');
    }
  }

  Future<void> _fetchProducts() async {
    try {
      final userProvider = Provider.of<UserProvider>(context, listen: false);
      final response = await Dio().get(
        'http://10.0.2.2:7128/api/products/',
        options: Options(headers: {
          'Authorization': 'Bearer ${userProvider.userToken}',
        }),
      );

      if (response.statusCode == 200) {
        setState(() {
          products = response.data;
          isLoadingProducts = false;
        });
      } else {
        logger.e('Failed to load products');
        _showError('Failed to load products');
      }
    } catch (e) {
      logger.e('Failed to load products');
      _showError('Error loading products: $e');
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: RefreshIndicator(
        onRefresh: () async {
          await _fetchCategories();
          await _fetchProducts();
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 16),
              _buildCategorySlideshow(),
              const SizedBox(height: 16),
              _buildProductGrid(),
            ],
          ),
        ),
      ),
      bottomNavigationBar: const MyNavigationBar(initialIndex: 0),
    );
  }

  // Category Slideshow
  Widget _buildCategorySlideshow() {
    if (isLoadingCategories) {
      return const Center(child: CircularProgressIndicator());
    }

    return SizedBox(
      height: 180, // Set height for the slideshow
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: categories.length,
        itemBuilder: (context, index) {
          final category = categories[index];
          return _buildCategoryCard(category);
        },
      ),
    );
  }

  // Single Category Card
  Widget _buildCategoryCard(dynamic category) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Image.network(
            category['category_image'],
            height: 120,
            width: 120,
            fit: BoxFit.cover,
          ),
          const SizedBox(height: 8),
          Text(
            category['name'],
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }

  // Product Grid
  Widget _buildProductGrid() {
    if (isLoadingProducts) {
      return const Center(child: CircularProgressIndicator());
    }

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
        return _buildProductCard(product);
      },
    );
  }

  // Single Product Card
  Widget _buildProductCard(dynamic product) {
    return Card(
      elevation: 2,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Image.network(
            product['image_1'],
            height: 120,
            fit: BoxFit.cover,
          ),
          const SizedBox(height: 8),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: Text(
              product['product_name'] ?? "Product Name",
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          const SizedBox(height: 8),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8.0),
            child: Text(
              "\$${product['price']}",
              style: const TextStyle(fontSize: 18, color: Colors.blue),
            ),
          ),
          const SizedBox(height: 10),
          Expanded(
            child: Center(
              child: ElevatedButton(
                  onPressed: () {
                    //add to cart function
                  },
                  style: ButtonStyle(
                    backgroundColor: WidgetStateProperty.all(Colors.blue),
                  ),
                  child: const Text(
                    "Add To Cart",
                    style: TextStyle(color: Colors.white),
                  )),
            ),
          )
        ],
      ),
    );
  }
}
