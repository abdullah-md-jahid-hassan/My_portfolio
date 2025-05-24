from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
]


# Serve static and media files in development
# This is only for development purposes. In production, you should use a proper web server.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
