import uuid
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django_order_app.models import Order

class OrderAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('order-list')

    def test_create_order(self):
        payload = {
            "user_id": str(uuid.uuid4()),
            "amount": "100.00",
            "currency": "USD"
        }
        res = self.client.post(self.url, payload, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
