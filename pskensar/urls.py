"""
URL configuration for pskensar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.utils.translation import override

def english_admin_view(view):
    def wrapper(*args, **kwargs):
        with override('en'):
            return view(*args, **kwargs)
    return wrapper

admin.site.login = english_admin_view(admin.site.login)

# Dil değiştirme için URL
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('kullanici/', include('users.urls')),
    path("payment/", include("payment.urls")),
    path('i18n/', include('django.conf.urls.i18n')),  # Dil değiştirme için gerekli
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Çok dilli URL yapısı
# urlpatterns += i18n_patterns(
    
#     prefix_default_language=True  # Varsayılan dili URL'ye ekleme
# )

# Statik dosyalar için
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

