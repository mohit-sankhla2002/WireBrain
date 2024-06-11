from django.core.mail import EmailMessage
import random
import os

class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()

def generate_otp():
    return str(random.randint(100000, 999999))