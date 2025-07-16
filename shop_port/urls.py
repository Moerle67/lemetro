from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop_port1.urls')),  # Haupt-Routing für den Shop
]

# WICHTIG: Damit Django Medien-Dateien im Entwicklungsmodus bereitstellt
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
