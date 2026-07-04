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

    def test_login_returns_token_for_product_creation(self):
        login_response = self.client.post(
            "/api/auth/login/",
            {
                "username": "merchantuser",
                "password": "strong-pass123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {login_response.data['token']}"
        )
        response = self.client.post(
            "/api/products/",
            {
                "name": "Token Product",
                "sku": "SKU456",
                "price": "12.50",
                "stock": 3,
                "description": "Created via token auth",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_with_merchant_profile_can_create_product(self):
        merchant_user = get_user_model().objects.create_user(
            username="merchantprofile",
            email="merchant-profile@example.com",
            password="strong-pass123",
            role="customer",
        )
        MerchantBusiness.objects.create(
            merchant=merchant_user,
            business_name="Profile Business",
            business_email="merchant-profile@example.com",
            phone="255700000001",
            category="retail",
            registration_number="REG456",
            tax_number="TAX456",
            annual_revenue="2000.00",
            address="Profile Address",
            city="Dodoma",
            country="Tanzania",
        )

        self.client.force_authenticate(merchant_user)
        response = self.client.post(
            "/api/products/",
            {
                "name": "Profile Product",
                "sku": "SKU789",
                "price": "15.00",
                "stock": 2,
                "description": "Created via merchant profile",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_without_merchant_profile_can_create_product(self):
        merchant_user = get_user_model().objects.create_user(
            username="nomerchantprofile",
            email="no-profile@example.com",
            password="strong-pass123",
            role="merchant",
        )

        self.client.force_authenticate(merchant_user)
        response = self.client.post(
            "/api/products/",
            {
                "name": "No Profile Product",
                "sku": "SKU000",
                "price": "10.00",
                "stock": 1,
                "description": "Auto-creates merchant profile",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(hasattr(merchant_user, "merchant_business"))
