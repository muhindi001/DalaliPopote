from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Invoice

from webhooks.events import dispatch_event


@receiver(post_save, sender=Invoice)
def invoice_handler(sender, instance, created, **kwargs):

    payload = {
        "invoice_id": str(instance.id),
        "transaction_id": str(instance.transaction.id),
        "total": str(instance.total),
        "status": instance.status,
    }

    if created:
        dispatch_event(instance.merchant, "invoice.created", payload)