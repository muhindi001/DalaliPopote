from rest_framework.permissions import BasePermission


class IsMerchantOwner(BasePermission):
    """
    Allows access only to authenticated merchants.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "merchant_business")
        )


class IsAdminOrMerchantOwner(BasePermission):
    """
    Admin can access everything.
    Merchant can access only their own resources.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        return obj.merchant == request.user.merchant_business