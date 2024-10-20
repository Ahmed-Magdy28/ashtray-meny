import 'package:ashtray_meny/classes/routes.dart';
import 'package:flutter/material.dart';
import 'package:ashtray_meny/controllers/sign_up_controller.dart';
import 'package:ashtray_meny/widgets/country_drop_down.dart';
import 'package:ashtray_meny/widgets/password_field.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final _emailController = TextEditingController();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>(); // Form key for validation

  String? selectedCountry;

  // Email Validator function
  String? _validateEmail(String value) {
    if (value.isEmpty || !value.contains('@')) {
      return 'Enter a valid email address';
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SizedBox(
        width: double.infinity,
        height: double.infinity,
        child: SingleChildScrollView(
          child: Center(
            child: Form(
              key: _formKey, // Assign the form key
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const Text("Sign Up", style: TextStyle(fontSize: 30)),
                  const SizedBox(height: 20),
                  Image.asset('assets/images/Icon.png',
                      width: 100, height: 100),
                  const SizedBox(height: 20),

                  // Email Field
                  Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: TextFormField(
                      controller: _emailController,
                      decoration: InputDecoration(
                        labelText: "Email",
                        hintText: "Enter your email",
                        border: OutlineInputBorder(
                          borderRadius:
                              BorderRadius.circular(12), // Rounded corners
                        ),
                      ),
                      validator: (value) => _validateEmail(value ?? ''),
                    ),
                  ),

                  // Username Field
                  Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: TextFormField(
                      controller: _usernameController,
                      decoration: InputDecoration(
                        labelText: "Username",
                        hintText: "Enter your username",
                        border: OutlineInputBorder(
                          borderRadius:
                              BorderRadius.circular(12), // Rounded corners
                        ),
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter a username';
                        }
                        return null;
                      },
                    ),
                  ),

                  // Country Drop Down
                  CountryDropDown(
                    initialCountry: "Egypt",
                    onCountryChanged: (country) {
                      selectedCountry = country;
                    },
                  ),

                  // Password Field (Using PasswordField Widget)
                  Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: PasswordField(
                      controller: _passwordController,
                      validator: (value) {
                        // Password validation is handled in the PasswordField widget
                        return null;
                      },
                    ),
                  ),

                  const SizedBox(height: 20),

                  // Link to log in
                  TextButton(
                    onPressed: () {
                      Navigator.pop(context);
                      Routes.openLogin(context: context);
                    },
                    child: const Text("Already have an account?"),
                  ),

                  const SizedBox(height: 20),

                  // Sign Up Button
                  ElevatedButton(
                    style: ButtonStyle(
                      backgroundColor: WidgetStateProperty.all(Colors.blue),
                      padding: WidgetStateProperty.all(
                        const EdgeInsets.symmetric(
                            vertical: 16.0, horizontal: 32.0), // Bigger padding
                      ),
                      minimumSize: WidgetStateProperty.all(
                          const Size(400, 50)), // Minimum size
                      shape: WidgetStateProperty.all(
                        RoundedRectangleBorder(
                          borderRadius:
                              BorderRadius.circular(12), // Rounded corners
                        ),
                      ),
                    ),
                    onPressed: () async {
                      if (_formKey.currentState!.validate()) {
                        bool success = await SignupController.createUser(
                          context: context,
                          email: _emailController.text,
                          password: _passwordController.text,
                          username: _usernameController.text,
                          country: selectedCountry ?? 'Egypt',
                        );
                        if (success) {
                          Navigator.pop(context);
                          Routes.openLogin(context: context);
                        }
                      }
                    },
                    child: const Text(
                      "Sign Up",
                      style: TextStyle(
                          color: Colors.white,
                          fontSize: 18), // Larger font size
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
