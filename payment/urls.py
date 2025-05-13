from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("checkout/", views.odeme, name="checkout"),
]
