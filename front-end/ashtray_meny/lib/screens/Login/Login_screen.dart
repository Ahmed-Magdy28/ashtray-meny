import 'package:ashtray_meny/classes/routes.dart';
import 'package:ashtray_meny/controllers/login_controller.dart';
import 'package:ashtray_meny/widgets/password_field.dart';
import 'package:flutter/material.dart';
import 'package:logger/logger.dart';
import 'package:ashtray_meny/providers/user_provider.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>(); // For form validation
  bool rememberMe = false; // Remember Me checkbox value

  var logger = Logger();
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    LoginController
        .loadUserCredentials(); // Load saved credentials when the screen loads
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: isLoading
          ? const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 20),
                  Text("Logging in..."),
                ],
              ),
            )
          : SingleChildScrollView(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    const SizedBox(height: 60),
                    const Text("Login",
                        style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Colors.black)),
                    const SizedBox(height: 20),
                    Image.asset('assets/images/Icon.png',
                        width: 120, height: 120),
                    const SizedBox(height: 30),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 32),
                      child: Form(
                        key: _formKey, // Wrap TextFields in Form for validation
                        child: Column(
                          children: [
                            TextFormField(
                              controller: _emailController,
                              decoration: const InputDecoration(
                                labelText: "Email/UserName",
                                hintText: "Enter your email or username",
                                border: OutlineInputBorder(),
                              ),
                              validator: (value) {
                                if (value == null || value.isEmpty) {
                                  return 'Please enter your email/username';
                                }
                                return null;
                              },
                            ),
                            const SizedBox(height: 20),
                            PasswordField(
                              controller: _passwordController,
                              validator: (value) {
                                if (value == null || value.isEmpty) {
                                  return 'Please enter your password';
                                }
                                return null;
                              },
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 10),
                    // Remember Me Checkbox
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 32),
                      child: Row(
                        children: [
                          Checkbox(
                            value: rememberMe,
                            onChanged: (value) {
                              setState(() {
                                rememberMe = value ?? false;
                              });
                            },
                          ),
                          const Text("Remember Me"),
                        ],
                      ),
                    ),
                    Align(
                      alignment: Alignment.centerRight,
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 32),
                        child: TextButton(
                          onPressed: () {
                            Routes.forgetPassword(context: context);
                          },
                          child: const Text(
                            "Forgot Password?",
                            style: TextStyle(color: Colors.black),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 30),
                    SizedBox(
                      width: double.infinity,
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 32),
                        child: ElevatedButton(
                          onPressed: () async {
                            if (_formKey.currentState?.validate() == true) {
                              setState(() {
                                isLoading = true;
                              });

                              // Call the login function
                              final loginData = await LoginController.login(
                                email: _emailController.text,
                                password: _passwordController.text,
                              );

                              if (loginData != null) {
                                // Extract token and user_id from loginData
                                final String? token = loginData['token'];
                                final String? userId = loginData['user_id'];

                                if (token != null || userId != null) {
                                  // Save token and fetch user data in UserProvider
                                  UserProvider()
                                      .getUserData(dataSnapShot: loginData);

                                  // Save email and password if Remember Me is checked
                                  await LoginController.saveUserCredentials(
                                    rememberMe: rememberMe,
                                    email: _emailController.text,
                                    password: _passwordController.text,
                                  );
                                }

                                // Navigate to the next screen after login success
                                Navigator.pop(context);
                                Routes.navigateToMainAndClearStack(
                                    context: context);
                              } else {
                                // Handle login failure
                                logger.e("Login failed");
                              }

                              setState(() {
                                isLoading = false;
                              });
                            }
                          },
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            backgroundColor: Colors.blueAccent,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ), // Button color
                          ),
                          child: const Text(
                            "Login",
                            style: TextStyle(fontSize: 18, color: Colors.white),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    TextButton(
                      onPressed: () {
                        Routes.openSignUp(context: context);
                      },
                      child: const Text(
                        "Don’t have an account? Sign Up",
                        style: TextStyle(color: Colors.black38),
                      ),
                    ),
                    const SizedBox(height: 20),
                  ],
                ),
              ),
            ),
    );
  }
}
