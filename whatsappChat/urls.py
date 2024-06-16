from django.urls import path
from . import views

urlpatterns = [
    path('indContact', views.indPhone.as_view()),
    path('sendMsg', views.sendMsg.as_view()),
    path('excelfile', views.csvPhone.as_view()),
]
