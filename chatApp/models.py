from django.db import models
from authApp import models as authModel

class conversation(models.Model):
    conversation_type = models.CharField(max_length=20)

    def __str__(self):
        return self.conversation_type

class messages(models.Model):
    conversation = models.ForeignKey(conversation, related_name='conversation', on_delete=models.CASCADE)
    sender = models.ForeignKey(authModel.User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(authModel.User, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content