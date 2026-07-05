from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Settlement

from webhooks.events import dispatch_event


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