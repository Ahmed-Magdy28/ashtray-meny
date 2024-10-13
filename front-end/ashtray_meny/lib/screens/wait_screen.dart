import 'package:ashtray_meny/classes/routes.dart';
import 'package:flutter/material.dart';

class WaitingScreen extends StatefulWidget {
  const WaitingScreen({super.key});

  @override
  State<WaitingScreen> createState() => _WaitingScreenState();
}

class _WaitingScreenState extends State<WaitingScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        color: Colors.red,
        child: Center(
          child: SizedBox(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Image.asset('assets/images/Icon.png', width: 100, height: 100),
                TextButton(
                    onPressed: () {
                      Routes.openLogin(context: context);
                    },
                    child: const Text("signIn screen",
                        style: TextStyle(color: Colors.white))),
                TextButton(
                    onPressed: () {
                      Routes.openSignUp(context: context);
                    },
                    child: const Text("signUp screen")),
                TextButton(
                    onPressed: () {
                      Routes.forgetPassword(context: context);
                    },
                    child: const Text("forgetPassword screen")),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
