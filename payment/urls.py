from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("checkout/", views.odeme, name="checkout"),
    path('services/', views.services, name='services'),
]
