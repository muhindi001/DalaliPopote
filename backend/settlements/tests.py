from django.test import TestCase

from merchants.models import MerchantBusiness
from payments.models import Payment
from customers.models import Customer
from transactions.models import Transaction
from settlements.models import Settlement


class SettlementSignalTests(TestCase):

    def setUp(self):
        self.merchant = MerchantBusiness.objects.create(
            business_name="Test Merchant",
            business_email="merchant@example.com",
            phone="1234567890",
            category="retail",
            registration_number="REG123",
            tax_number="TAX123",
            annual_revenue=1000,
            address="Test Address",
            city="Test City",
            country="Test Country",
        )
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
        )

    def test_settlement_is_created_for_successful_transaction(self):
        payment = Payment.objects.create(
            merchant=self.merchant,
            customer=self.customer,
            amount=100.00,
            currency="TZS",
            status="SUCCESS",
        )

        transaction = Transaction.objects.get(payment=payment)
        self.assertEqual(transaction.status, "SUCCESS")

        settlement = Settlement.objects.get(transaction=transaction)
        self.assertEqual(settlement.gross_amount, payment.amount)
        self.assertEqual(settlement.currency, payment.currency)
        self.assertEqual(settlement.status, "PENDING")
