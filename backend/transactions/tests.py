from django.apps import apps
from django.db.models.signals import post_save
from django.test import SimpleTestCase

from payments.models import Payment
from transactions.apps import TransactionsConfig


class TransactionSignalRegistrationTests(SimpleTestCase):
    def test_payment_success_signal_is_registered(self):
        config = TransactionsConfig("transactions", apps)
        config.ready()

        receivers = post_save._live_receivers(Payment)
        self.assertTrue(
            any(getattr(receiver, "__name__", None) == "create_transaction_on_success" for receiver in receivers)
        )
