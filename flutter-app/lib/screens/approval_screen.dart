import 'package:flutter/material.dart';

class ApprovalScreen extends StatelessWidget {
  final String orderId;
  ApprovalScreen({required this.orderId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Approve $orderId')),
      body: Center(child: ElevatedButton(
        child: const Text('Approve'),
        onPressed: () {/* call API */},
      )),
    );
  }
}
