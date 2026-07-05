import json
from django.utils import timezone

try:
    import requests
except ImportError:  # pragma: no cover - handled at runtime
    requests = None


class WebhookService:

    @staticmethod
    def send_event(webhook, event, payload):

        if webhook.status != "ACTIVE":
            return None

        if webhook.event != event:
            return None

        headers = {
            "Content-Type": "application/json",
        }

        if webhook.secret:
            headers["X-Webhook-Secret"] = webhook.secret

        if requests is None:
            webhook.last_response_code = "ERROR"
            webhook.last_attempt_at = timezone.now()
            webhook.save(update_fields=[
                "last_response_code",
                "last_attempt_at"
            ])
            return None

        try:
            response = requests.post(
                webhook.url,
                data=json.dumps(payload),
                headers=headers,
                timeout=5
            )

            webhook.last_response_code = str(response.status_code)
            webhook.last_attempt_at = timezone.now()
            webhook.save(update_fields=[
                "last_response_code",
                "last_attempt_at"
            ])

            return response.status_code

        except Exception as e:
            webhook.last_response_code = "ERROR"
            webhook.last_attempt_at = timezone.now()
            webhook.save(update_fields=[
                "last_response_code",
                "last_attempt_at"
            ])

            return None