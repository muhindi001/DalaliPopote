from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Settlement
from .services import SettlementService
from transactions.models import Transaction

from webhooks.events import dispatch_event


@receiver(post_save, sender=Transaction)
def create_settlement_on_transaction_success(sender, instance, created, **kwargs):
    if instance.status != "SUCCESS":
        return

    if hasattr(instance, "settlement"):
        return

    SettlementService.create_settlement_from_transaction(instance)


@receiver(post_save, sender=Settlement)
def settlement_handler(sender, instance, created, **kwargs):

    payload = {
        "settlement_id": str(instance.id),
        "transaction_id": str(instance.transaction.id),
        "amount": str(instance.net_amount),
        "status": instance.status,
    }

    if not created and instance.status == "COMPLETED":
        dispatch_event(instance.merchant, "settlement.completed", payload)