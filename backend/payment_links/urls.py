from django.urls import path
from .views import (
    PaymentLinkListCreateView,
    PaymentLinkDetailView,
)

urlpatterns = [
    path(
        "",
        PaymentLinkListCreateView.as_view(),
        name="payment-link-list",
    ),
    path(
        "<int:pk>/",
        PaymentLinkDetailView.as_view(),
        name="payment-link-detail",
    ),
]