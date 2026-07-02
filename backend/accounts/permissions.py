from rest_framework.permissions import BasePermission


class IsMerchant(BasePermission):

    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False

        role = getattr(request.user, "role", None)
        if isinstance(role, str):
            role = role.lower()

        return role in {"merchant", "merchant_user", "seller", "vendor"}