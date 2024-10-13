import 'package:flutter/material.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: SingleChildScrollView(
      child: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
            gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [Colors.blue, Colors.blueGrey])),
        child: Center(
          child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const Text("Sign Up", style: TextStyle(fontSize: 30)),
                const SizedBox(height: 20),
                Image.asset('assets/images/Icon.png', width: 100, height: 100),
                const SizedBox(
                  height: 20,
                ),
                const Padding(
                  padding: EdgeInsets.all(12.0),
                  child: TextField(
                    decoration: InputDecoration(label: Text("Email")),
                  ),
                ),
                const Padding(
                  padding: EdgeInsets.all(8.0),
                  child: TextField(
                    decoration: InputDecoration(
                        labelText: "UserName", hintText: "username"),
                  ),
                ),
                const Padding(
                  padding: EdgeInsets.all(8.0),
                  child: TextField(
                    decoration: InputDecoration(hintText: "Password"),
                  ),
                ),
                const Padding(
                  padding: EdgeInsets.all(8.0),
                  child: TextField(
                    decoration: InputDecoration(hintText: "Confirm Password"),
                  ),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                    style: const ButtonStyle(
                        backgroundColor:
                            WidgetStatePropertyAll<Color>(Colors.blue)),
                    onPressed: () {},
                    child: const Text(
                      "Sign Up",
                      style: TextStyle(color: Colors.white),
                    )),
              ]),
        ),
      ),
    ));
  }
}
