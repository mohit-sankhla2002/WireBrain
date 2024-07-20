from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from heyoo import WhatsApp
from . import serializers
from . import models
from . import renderers
from . import webhook
import tempfile
import os
import json

AUTH_TOKEN = "EAAL7og371v4BOzH3qCP6o1o2WdIfdwZBU0M2Oy9xhqSK9IwJ1jQJjs1P69z3Kq9dchPdpuGc0MpL4Wna2XMxHFXivD4qPfDS1zZA7H7SY60H8IzmGh4wTFQ4H4Uz5SZAlCmYDiLZCRK3vDaRrUomNpiKFH6KfD2qTcnAceRRIZCFiUz3GOgVZBoMHl0ZAOXvz7mgAZDZD"
PHONE_ID = "275772712289918"

class someFunction(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer=serializers.credentialSerializer(context={'user':request.user})
        try:
            credentials=serializer.get_credentials()
            messenger = WhatsApp(token=credentials['auth_token'], phone_number_id=credentials['phone_number_id'])
            return Response({'msg': "Credentials Obtained"}, status=status.HTTP_202_ACCEPTED)
        except serializers.ValidationError as e:
            return Response({'error': "Invalid Access Token"}, status=status.HTTP_400_BAD_REQUEST)

messenger = WhatsApp(token=AUTH_TOKEN, phone_number_id=PHONE_ID)

class getTemplates(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.getTemplatesSerializer(context={'user': request.user})
        try:
            message_templates = serializer.get_message_templates()
            return Response({'templates': message_templates}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

def sendMedia(media, phone, mediaType, query):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(media.name)[1]) as temp_file:
        for chunk in media.chunks():
            temp_file.write(chunk)
        media_id = messenger.upload_media(
            media=temp_file.name
        )['id']
        kwargs = {
            mediaType: media_id,
            'recipient_id': phone,
            'link': False
        }
        response = getattr(messenger,query)(**kwargs)
        output = {'response': response, 'media_id': media_id}
        return output

class contactView(APIView):
    renderer_classes = [renderers.MessageRenderers]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = serializers.contactSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class csvPhone(APIView):
    renderer_classes = [renderers.MessageRenderers]
    def post(self, request, format=None):
        serializer = serializers.excelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save();
            return Response({'msg': "Data Saved"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class sendTemplate(APIView):
    renderer_classes = [renderers.MessageRenderers]
    def post(self, request):
        serializer = serializers.PhoneSerializer(data=request.data)
        if serializer.is_valid():
            mobile = request.data['phone']
            response = messenger.send_template(template="hello_world", recipient_id=mobile, components=[])
            print(response)
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendText(APIView):
    def post(self, request):
        serializer = serializers.MessageSerializer(data=request.data)
        if serializer.is_valid():
            mobile = request.data['phone']
            message = request.data['message']
            response = messenger.send_message(message=message, recipient_id=mobile)
            message_id = response['messages'][0]['id']
            messenger.set_message(message_id=message_id, message_content=message, message_type='text')
            
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendImage(APIView):
    def post(self, request):
        serializer = serializers.MediaSerializer(data=request.data)
        if serializer.is_valid():
            media = request.FILES['media']
            phone = request.data['phone']
            output = sendMedia(media=media, phone=phone, mediaType='image', query= 'send_image')
            response=output['response']
            message_id = response['messages'][0]['id']
            messenger.set_message(message_id=message_id, message_type='image', message_content=output['media_id'])
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendVideo(APIView):
    def post(self, request):
        serializer = serializers.MediaSerializer(data=request.data)
        if serializer.is_valid():
            media = request.FILES['media']
            phone = request.data['phone']
            output = sendMedia(media=media, phone= phone, mediaType='video', query='send_video')
            response=output['response']
            message_id = response['messages'][0]['id']
            messenger.set_message(message_id=message_id, message_type='video', message_content=output['media_id'])
            print("Message store is: ",messenger.messages_store)
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendPdf(APIView):
    def post(self, request):
        serializer = serializers.MediaSerializer(data=request.data)
        if serializer.is_valid():
            media = request.FILES['media']
            phone = request.data['phone']
            output = sendMedia(media=media, phone= phone, mediaType='document', query="send_document")
            response = output['response']
            message_id = response['messages'][0]['id']
            messenger.set_message(message_id=message_id, message_type='document', message_content=output['media_id'])
            print(messenger.messages_store)
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendAudio(APIView):
    def post(self, request):
        serializer = serializers.MediaSerializer(data=request.data)
        if serializer.is_valid():
            media = request.FILES['media']
            phone = request.data['phone']
            output = sendMedia(media=media, phone= phone, mediaType='audio', query="send_audio")
            response = output['response']
            message_id = response['messages'][0]['id']
            messenger.set_message(message_id=message_id, message_type='audio', message_content=output['media_id'])
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendLocation(APIView):
    def post(self, request):
        phone = request.data['phone']
        response = messenger.send_location(
        lat=1.29,
        long=103.85,
        name="Singapore",
        address="Singapore",
        recipient_id=phone,
    )
        print(response)
        return Response({'msg': response}, status=status.HTTP_200_OK)
        
class WebhookView(APIView):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        webhookCall = webhook.Webhook(data=data, messenger=messenger)
        if 'statuses' in data['entry'][0]['changes'][0]['value']:
            webhookCall.sendMessage()
        else:
            webhookCall.receiveMessage()
        response_message = 'Message received and stored successfully.'
        return Response({'status': 'success', 'message': response_message}, status=status.HTTP_201_CREATED)
    

class get_chat_by_id(APIView):
    def get(self, request, format=None): 
        phone = request.query_params.get('phone')
        messages = models.chats.find()
        chat_history = []
        for message in messages:
            value = message['entry'][0]['changes'][0]['value']
            msgEndpoint = message['entry'][0]['changes'][0]['value']['messages'][0]
            mediaId=""
            textBody=""
            if 'text' in msgEndpoint: textBody = msgEndpoint['text']['body']
            elif 'image' in msgEndpoint:mediaId = msgEndpoint['image']['id']
            elif 'video' in msgEndpoint:mediaId = msgEndpoint['video']['id']
            elif 'document' in msgEndpoint:mediaId = msgEndpoint['document']['id']
            elif 'audio' in msgEndpoint:mediaId = msgEndpoint['audio']['id']
            messageType = msgEndpoint['type']
            content = textBody if textBody else messenger.query_media_url(mediaId)
            if 'statuses' in value and value['statuses'][0]['recipient_id'] == phone:
                statusLog = value['status_log']
                msg_entry = {
                                "from": phone,
                                "to": value['metadata']['phone_number_id'],
                                "type": messageType,
                                "body": content,
                                "status": statusLog
                            }
    
            elif value['contacts'][0]['wa_id'] == phone and value['metadata']['phone_number_id'] == phone:
                timestamp = msgEndpoint['timestamp']
                msg_entry = {
                                "from": value['metadata']['phone_number_id'],
                                "to": phone,
                                "type": messageType,
                                "body": content,
                                "status": timestamp
                            }
            chat_history.append(msg_entry)
        print(chat_history)
        return Response({'msg': "success"}, status=status.HTTP_200_OK)
    
class getTeamChats(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user=request.user
        try:
            records = models.chats.find({'teamId': user.team.id}, {'_id': 1, 'recipientId': 1, 'universalTimestamp': 1})
            records = list(records)
            for record in records:
                record['_id'] = str(record['_id'])
            return Response({'records': records}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Unauthorized User"}, status=status.HTTP_401_UNAUTHORIZED)
    
class get_all_chats(APIView):
    def post(self, request, format=None):
        sender_id = request.data['sender']
        receiver_id = request.data['receiver']
        messages = models.chats.find()
        chat_history = []
        for message in messages:
            value = message['entry'][0]['changes'][0]['value']
            msgEndpoint = message['entry'][0]['changes'][0]['value']['messages'][0]
            mediaId=""
            textBody=""
            if 'text' in msgEndpoint: textBody = msgEndpoint['text']['body']
            elif 'image' in msgEndpoint:mediaId = msgEndpoint['image']['id']
            elif 'video' in msgEndpoint:mediaId = msgEndpoint['video']['id']
            elif 'document' in msgEndpoint:mediaId = msgEndpoint['document']['id']
            elif 'audio' in msgEndpoint:mediaId = msgEndpoint['audio']['id']
            messageType = msgEndpoint['type']
            content = textBody if textBody else messenger.query_media_url(mediaId)
            if 'statuses' in value and value['statuses'][0]['recipient_id'] == sender_id:
                statusLog = value['status_log']
                msg_entry = {
                                "from": receiver_id,
                                "to": sender_id,
                                "type": messageType,
                                "body": content,
                                "status": statusLog
                            }
    
            elif value['contacts'][0]['wa_id'] == sender_id and value['metadata']['phone_number_id'] == receiver_id:
                timestamp = msgEndpoint['timestamp']
                msg_entry = {
                                "from": sender_id,
                                "to": receiver_id,
                                "type": messageType,
                                "body": content,
                                "status": timestamp
                            }
            chat_history.append(msg_entry)
        print(chat_history)
        return Response({'msg': chat_history}, status=status.HTTP_200_OK)
    

class get_contacts_by_id(APIView): 
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        contacts = models.Contact.objects.filter(user=request.user.id)

        if (len(contacts) == 0):
            return Response({'msg': 'No contacts found with given user id'}, status=status.HTTP_404_NOT_FOUND)

        print(contacts)
        return Response({'contacts': list(contacts.values())}, status=status.HTTP_200_OK)
        

