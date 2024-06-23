from django.urls import path
from . import views

urlpatterns = [
    path('indContact', views.indPhone.as_view()),
    path('template-send', views.sendTemplate.as_view()),
    path('message-send', views.sendMessage.as_view()),
    path('excelfile', views.csvPhone.as_view()),
]
