from django.db.models.signals import post_save
from django.dispatch import receiver
from webhooks.events import dispatch_event
from .models import Refund


@receiver(post_save, sender=Refund)
def refund_status_handler(sender, instance, created, **kwargs):

    if created:
        print(
            f"[REFUND CREATED] "
            f"{instance.refund_reference}"
        )

    else:
        print(
            f"[REFUND UPDATED] "
            f"{instance.refund_reference} -> {instance.status}"
        )

        if instance.status == "SUCCESS":

            print(
                f"[REFUND SUCCESS] "
                f"{instance.payment.payment_reference}"
            )

            # Future integrations:
            #
            # 1. Send webhook
            # 2. Notify customer
            # 3. Send merchant email
            # 4. Create audit log
            # 5. Push notification
            

@receiver(post_save, sender=Refund)
def refund_handler(sender, instance, created, **kwargs):

    payload = {
        "refund_id": str(instance.refund_reference),
        "payment_id": instance.payment.id,
        "amount": str(instance.amount),
        "status": instance.status,
    }

    if created:
        dispatch_event(instance.merchant, "refund.created", payload)

    if not created and instance.status == "SUCCESS":
        dispatch_event(instance.merchant, "payment.refunded", payload)