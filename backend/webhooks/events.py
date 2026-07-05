from .models import Webhook
from .services import WebhookService


def dispatch_event(merchant, event, payload):

    webhooks = Webhook.objects.filter(
        merchant=merchant,
        event=event,
        status="ACTIVE"
    )

    for webhook in webhooks:
        WebhookService.send_event(
            webhook=webhook,
            event=event,
            payload=payload
        )