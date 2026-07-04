from django.db.models.signals import post_save
from django.dispatch import receiver

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