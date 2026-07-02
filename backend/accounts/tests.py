# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient

# from .models import User


# class LoginViewTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_login_with_email_and_password_returns_tokens(self):
#         User.objects.create_user(
#             username='demo_user',
#             email='demo@example.com',
#             password='StrongPass123!',
#             role='customer',
#             phone='0712345678',
#         )

#         response = self.client.post(
#             reverse('login'),
#             {
#                 'email': 'demo@example.com',
#                 'password': 'StrongPass123!',
#             },
#             format='json',
#         )

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('access', response.data)
#         self.assertIn('refresh', response.data)
