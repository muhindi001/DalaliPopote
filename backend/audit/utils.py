from .models import AuditLog


def log_activity(request, action, details=None):
    AuditLog.objects.create(
        user=request.user,
        action=action,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        details=details or {},
    )