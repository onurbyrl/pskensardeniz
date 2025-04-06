from django.urls import path
from . import views

app_name = 'core'


urlpatterns = [
    path('', views.index, name='home'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('ilkelerimiz/', views.ilkelerimiz, name='ilkelerimiz'),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('<slug:slug>/', views.uygulama_detay, name='uygulama_detay'),
    path("search/", views.search_results, name="search_results"),
]