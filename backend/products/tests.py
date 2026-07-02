from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from merchants.models import MerchantBusiness


class ProductPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="merchantuser",
            email="merchant@example.com",
            password="strong-pass123",
            role="merchant",
        )
        self.merchant = MerchantBusiness.objects.create(
            merchant=self.user,
            business_name="Test Business",
            business_email="merchant@example.com",
            phone="255700000000",
            category="retail",
            registration_number="REG123",
            tax_number="TAX123",
            annual_revenue="1000.00",
            address="Test Address",
            city="Dar es Salaam",
            country="Tanzania",
        )

    def test_product_list_is_public(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_merchant_can_create_product(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            "/api/products/",
            {
                "name": "Test Product",
                "sku": "SKU123",
                "price": "10.00",
                "stock": 5,
                "description": "A test product",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
