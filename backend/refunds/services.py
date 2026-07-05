from decimal import Decimal
from django.db import models, transaction
from django.utils import timezone

from .models import Refund


class RefundService:

    @staticmethod
    @transaction.atomic
    def process_refund(refund: Refund):
        """
        Process a refund.

        Currently simulates a successful gateway refund.
        Replace this section with actual payment gateway logic later.
        """

        payment = refund.payment

        # Prevent duplicate processing
        if refund.status == "SUCCESS":
            return refund

        # Simulate gateway approval
        refund.status = "SUCCESS"
        refund.processed_at = timezone.now()
        refund.gateway_reference = (
            f"RFD-{refund.refund_reference.hex[:12].upper()}"
        )
        refund.save()

        # Calculate total successful refunds
        total_refunded = (
            payment.refunds
            .filter(status="SUCCESS")
            .exclude(pk=refund.pk)
            .aggregate(total=models.Sum("amount"))["total"]
            or Decimal("0.00")
        )

        total_refunded += refund.amount

        # Update payment status
        if total_refunded >= payment.amount:
            payment.status = "REFUNDED"
        else:
            payment.status = "SUCCESS"

        payment.save(update_fields=["status"])

        return refund

    @staticmethod
    @transaction.atomic
    def cancel_refund(refund: Refund):

        if refund.status == "SUCCESS":
            raise Exception(
                "Successful refunds cannot be cancelled."
            )

        refund.status = "CANCELLED"
        refund.save(update_fields=["status"])

        return refund

    @staticmethod
    def refundable_balance(payment):

        total = (
            payment.refunds
            .filter(status="SUCCESS")
            .aggregate(total=models.Sum("amount"))["total"]
            or Decimal("0.00")
        )

        return payment.amount - total