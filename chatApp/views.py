from django.http import HttpResponse
from . import models

def chatDisplay(request):
    chats = models.messages.objects.filter(sender_id=17)
    messages=[]
    for chat in chats:
        message = chat.content
        messages.append(message)
    print(messages)
    return HttpResponse(messages)