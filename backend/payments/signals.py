from django.db.models.signals import post_save
from django.dispatch import receiver
from webhooks.events import dispatch_event
from .models import Payment


@receiver(post_save, sender=Payment)
def payment_status_handler(sender, instance, created, **kwargs):

    # New payment created
    if created:
        print(f"[PAYMENT CREATED] {instance.payment_reference}")

    # Payment updated
    else:
        print(f"[PAYMENT UPDATED] {instance.payment_reference} -> {instance.status}")

        # Future logic placeholder:
        # if instance.status == "SUCCESS":
        #     create_transaction(instance)
        #     generate_invoice(instance)
        
@receiver(post_save, sender=Payment)
def payment_status_handler(sender, instance, created, **kwargs):

    payload = {
        "payment_id": instance.id,
        "amount": str(instance.amount),
        "currency": instance.currency,
        "status": instance.status,
        "reference": instance.payment_reference,
    }

    if created:
        dispatch_event(instance.merchant, "payment.created", payload)

    if not created and instance.status == "SUCCESS":
        dispatch_event(instance.merchant, "payment.success", payload)

    if not created and instance.status == "FAILED":
        dispatch_event(instance.merchant, "payment.failed", payload)