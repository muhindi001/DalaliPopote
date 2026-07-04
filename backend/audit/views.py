from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        # Admin/staff can see all logs
        if self.request.user.is_staff:
            return AuditLog.objects.all().order_by("-created_at")

        # Regular users only see their own logs
        return AuditLog.objects.filter(
            user=self.request.user
        ).order_by("-created_at")