from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path('giris-yap/', views.user_login, name='login'),
    path('kayit-ol/', views.register, name='register'),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path('randevu-olustur/', views.randevu_olustur, name='randevu_olustur'),
]