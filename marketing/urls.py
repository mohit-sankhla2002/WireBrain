from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('authApp.urls')),
    path('api/team/', include('createTeam.urls')),
    path('api/chat/', include('chatApp.urls')),
    path('api/wchat/', include('whatsappChat.urls'))
]
