from django.db.models.signals import post_save
from django.dispatch import receiver
from invoices.services import create_invoice_from_transaction
from payments.models import Payment
from .models import Transaction


@receiver(post_save, sender=Payment)
def create_transaction_on_success(sender, instance, created, **kwargs):

    if instance.status != "SUCCESS":
        return

    if Transaction.objects.filter(payment=instance).exists():
        return

    transaction = Transaction.objects.create(
        payment=instance,
        merchant=instance.merchant,
        customer=instance.customer,
        reference=f"TXN-{instance.payment_reference}",
        gateway_reference=instance.gateway_reference,
        gross_amount=instance.amount,
        fee=0,
        net_amount=instance.amount,
        currency=instance.currency,
        status="SUCCESS",
        gateway="INTERNAL",
    )

    # Create invoice automatically
    create_invoice_from_transaction(transaction)  
