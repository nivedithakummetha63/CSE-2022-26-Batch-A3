from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import custom admin configuration
import roomieradar.admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    # Authentication
    path('accounts/', include('accounts.urls')),
    # Main App ( /app/ )
    path('', include('base.urls')),
    # Chat module
    path('chat/', include('chat.urls')),
    # Rooms & booking
    path('rooms/', include('roomieradar_app.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
