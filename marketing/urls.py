from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('authApp.urls')),
    path('api/team/', include('createTeam.urls')),
    path('api/chat/', include('chatApp.urls')),
    path('api/wchat/', include('whatsappChat.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
