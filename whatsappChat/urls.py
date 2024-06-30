from django.urls import path
from . import views

urlpatterns = [
    path('contacts', views.contactView.as_view()),
    path('template-send', views.sendTemplate.as_view()),
    path('text-send', views.sendText.as_view()),
    path('image-send', views.sendImage.as_view()),
    path('video-send', views.sendVideo.as_view()),
    path('audio-send', views.sendAudio.as_view()),
    path('doc-send', views.sendPdf.as_view()),
    path('location-send', views.sendLocation.as_view()),
    path('data-send', views.WebhookView.as_view()),
    path('excelfile', views.csvPhone.as_view()),
    path('get-chats', views.get_all_chats.as_view()),
]
