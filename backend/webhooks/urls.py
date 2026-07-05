from django.urls import path

from .views import (
    WebhookListCreateView,
    WebhookDetailView,
)

urlpatterns = [
    path("", WebhookListCreateView.as_view(), name="webhook-list-create"),
    path("<uuid:pk>/", WebhookDetailView.as_view(), name="webhook-detail"),
]