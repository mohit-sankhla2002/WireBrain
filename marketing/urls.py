from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('authApp.urls')),
    path('api/chat/', include('chatApp.urls'))
]
