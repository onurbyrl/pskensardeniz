from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path('giris-yap/', views.user_login, name='login'),
    path('kayit-ol/', views.register, name='register'),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path('randevu-olustur/', views.randevu_olustur, name='randevu_olustur'),
    path('profil/', views.user_profile, name='profile'),
    path("sifremi-unuttum/", views.password_reset_view, name="password_reset_page"),
    path("sifremi-unuttum/ajax/", views.password_reset_ajax, name="password_reset_ajax"),
    path('sifre-yenile/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]