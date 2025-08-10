import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_app/main.dart' as app;

void main() {
  testWidgets('App loads', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    expect(find.text('Orders'), findsOneWidget);
  });
}
