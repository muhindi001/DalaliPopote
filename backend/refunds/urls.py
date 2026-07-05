from django.urls import path

from .views import (
    RefundListCreateView,
    RefundDetailView,
)

urlpatterns = [
    path(
        "",
        RefundListCreateView.as_view(),
        name="refund-list-create",
    ),

    path(
        "<int:pk>/",
        RefundDetailView.as_view(),
        name="refund-detail",
    ),
]