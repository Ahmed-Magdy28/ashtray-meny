import 'package:ashtray_meny/classes/routes.dart';
import 'package:ashtray_meny/widgets/navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ashtray_meny/providers/user_provider.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  @override
  Widget build(BuildContext context) {
    // Access the UserProvider to get user data
    final userProvider = Provider.of<UserProvider>(context);

    return WillPopScope(
      onWillPop: () async {
        // Return to MainScreen instead of going back step by step
        Routes.navigateToMainAndClearStack(context: context);
        return false; // Prevent the default back button behavior
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Profile'),
        ),
        body: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                // Profile Picture
                CircleAvatar(
                  radius: 50,
                  backgroundImage: userProvider.userImage.isNotEmpty
                      ? NetworkImage(userProvider.userImage)
                      : const AssetImage('assets/images/default_avatar.png')
                          as ImageProvider, // Default image if no profile picture
                ),
                const SizedBox(height: 16),

                // User Name
                Text(
                  userProvider.userName.isNotEmpty
                      ? userProvider.userName
                      : 'User Name',
                  style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),

                // User Email
                Text(
                  userProvider.userEmail.isNotEmpty
                      ? userProvider.userEmail
                      : 'No Email Provided',
                  style: const TextStyle(
                    fontSize: 16,
                    color: Colors.grey,
                  ),
                ),
                const SizedBox(height: 16),

                // User Country
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.location_on, color: Colors.blue),
                    const SizedBox(width: 8),
                    Text(
                      userProvider.userCountry.isNotEmpty
                          ? userProvider.userCountry
                          : 'No Country Specified',
                      style: const TextStyle(
                        fontSize: 16,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),

                // About User
                if (userProvider.aboutUser.isNotEmpty) ...[
                  const Text(
                    'About Me',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    userProvider.aboutUser,
                    textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 16),
                  ),
                  const SizedBox(height: 16),
                ],

                // Orders Summary
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildSummaryTile(
                      title: 'Orders Completed',
                      value: userProvider.ordersCompleted.toString(),
                    ),
                    _buildSummaryTile(
                      title: 'Current Orders',
                      value: userProvider.ordersNow.toString(),
                    ),
                  ],
                ),
                const SizedBox(height: 32),

                // Edit Profile Button
                ElevatedButton(
                  onPressed: () {
                    Routes.toEditProfile(context: context);
                  },
                  child: const Text('Edit Profile'),
                ),
              ],
            ),
          ),
        ),
        bottomNavigationBar: const MyNavigationBar(
          initialIndex: 1,
        ),
      ),
    );
  }

  // Widget to display summary data (like orders completed)
  Widget _buildSummaryTile({required String title, required String value}) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          title,
          style: const TextStyle(
            fontSize: 16,
            color: Colors.grey,
          ),
        ),
      ],
    );
  }
}
