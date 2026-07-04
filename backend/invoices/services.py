from .models import Invoice


def generate_invoice_number(transaction_id):
    return f"INV-{transaction_id}"


def create_invoice_from_transaction(transaction):

    if hasattr(transaction, "invoice"):
        return transaction.invoice

    subtotal = transaction.gross_amount
    tax = 0
    discount = 0
    total = subtotal + tax - discount

    invoice = Invoice.objects.create(
        invoice_number=generate_invoice_number(transaction.reference),
        merchant=transaction.merchant,
        customer=transaction.customer,
        transaction=transaction,
        subtotal=subtotal,
        tax=tax,
        discount=discount,
        total=total,
        currency=transaction.currency,
        status="PAID",
    )

    return invoice