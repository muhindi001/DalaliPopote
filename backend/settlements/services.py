from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from .models import Settlement


class SettlementService:

    PLATFORM_FEE_RATE = Decimal("0.02")  # 2%

    @staticmethod
    @transaction.atomic
    def create_settlement_from_transaction(transaction_obj):

        if hasattr(transaction_obj, "settlement"):
            return transaction_obj.settlement

        merchant = transaction_obj.merchant

        gross_amount = transaction_obj.gross_amount

        # Platform fee calculation
        platform_fee = gross_amount * SettlementService.PLATFORM_FEE_RATE

        net_amount = gross_amount - platform_fee

        settlement = Settlement.objects.create(
            merchant=merchant,
            transaction=transaction_obj,
            reference=f"SETT-{transaction_obj.reference}",
            gross_amount=gross_amount,
            platform_fee=platform_fee,
            net_amount=net_amount,
            currency=transaction_obj.currency,
            status="PENDING",
        )

        return settlement

    @staticmethod
    @transaction.atomic
    def process_settlement(settlement: Settlement):

        if settlement.status == "COMPLETED":
            return settlement

        settlement.status = "PROCESSING"
        settlement.save(update_fields=["status"])

        # Simulate payout processing (bank/mobile money/etc.)
        settlement.status = "COMPLETED"
        settlement.settled_at = timezone.now()
        settlement.save(update_fields=["status", "settled_at"])

        return settlement

    @staticmethod
    def calculate_fee(amount: Decimal) -> Decimal:
        return amount * SettlementService.PLATFORM_FEE_RATE

    @staticmethod
    def calculate_net(amount: Decimal) -> Decimal:
        return amount - SettlementService.calculate_fee(amount)