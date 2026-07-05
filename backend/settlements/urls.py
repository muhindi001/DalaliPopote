from django.urls import path

from .views import (
    SettlementListView,
    SettlementDetailView,
    SettlementProcessView,
)

urlpatterns = [
    path("", SettlementListView.as_view(), name="settlement-list"),
    path("<uuid:pk>/", SettlementDetailView.as_view(), name="settlement-detail"),

    # Manual payout trigger
    path("<uuid:pk>/process/", SettlementProcessView.as_view(), name="settlement-process"),
]