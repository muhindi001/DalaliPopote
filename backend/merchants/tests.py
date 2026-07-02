from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class MerchantAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_merchant_registration_does_not_require_authentication(self):
        response = self.client.post(
            '/api/merchant/register/',
            {
                'business_name': 'Test Business',
                'business_email': 'merchant@example.com',
                'phone': '255700000000',
                'category': 'retail',
                'registration_number': 'REG123',
                'tax_number': 'TAX123',
                'annual_revenue': '1000.00',
                'address': 'Test Address',
                'city': 'Dar es Salaam',
                'country': 'Tanzania',
            },
            format='json',
        )

        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
