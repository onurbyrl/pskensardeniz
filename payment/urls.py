from django.urls import path
from .views import create_payment, payment_callback

app_name = "payment"

urlpatterns = [
    path("checkout/", create_payment, name="checkout"),
    path("callback/", payment_callback, name="callback"),
]
