from django.urls import path
from .views import (
    MerchantBusinessCreateView,
    MerchantProfileView,
)

urlpatterns = [
    path("register/",MerchantBusinessCreateView.as_view()),
    path("profile/",MerchantProfileView.as_view()),
]