import 'package:flutter/material.dart';
import 'approval_screen.dart';

class OrderListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final orders = ['order1','order2']; # 模擬資料
    return Scaffold(
      appBar: AppBar(title: const Text('Orders')),
      body: ListView(
        children: orders.map((o) => ListTile(
          title: Text(o),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ApprovalScreen(orderId: o))),
        )).toList(),
      ),
    );
  }
}
