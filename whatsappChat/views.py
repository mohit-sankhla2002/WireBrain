from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from heyoo import WhatsApp
from . import serializers
from . import models
from . import renderers
import logging
import tempfile
import os
import json

AUTH_TOKEN = "EAAL7og371v4BOzH3qCP6o1o2WdIfdwZBU0M2Oy9xhqSK9IwJ1jQJjs1P69z3Kq9dchPdpuGc0MpL4Wna2XMxHFXivD4qPfDS1zZA7H7SY60H8IzmGh4wTFQ4H4Uz5SZAlCmYDiLZCRK3vDaRrUomNpiKFH6KfD2qTcnAceRRIZCFiUz3GOgVZBoMHl0ZAOXvz7mgAZDZD"
PHONE_ID = "275772712289918"
db = settings.MONGO_DB
collection = db['wchatApp']

messenger = WhatsApp(token=AUTH_TOKEN, phone_number_id=PHONE_ID)

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
    def saveMessage(self, messageId, data, report):
        query = {"entry.changes.value.messages.id": messageId}
        document = models.chats.find_one(query)
        if document:
            models.chats.update_one(
            query,
            {"$push": {"entry.$[].changes.$[].value.status_log":report}}
            )
        else:
            data['entry'][0]['changes'][0]['value']['status_log'] = [report]
            models.chats.insert_one(data)
    
    def setMedia(self, contentId, timestamp, heading, mediaType, mediaId):
        new_messages = {
            'messages': [
            {
                'id': contentId, 
                'timestamp': timestamp, 
                heading: {
                'mime_type': mediaType,  
                'id': mediaId
                },
                'type': heading
            }
        ]}
        return new_messages

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        changed_field = messenger.changed_field(data)

        if changed_field == "messages":
            new_message = messenger.get_mobile(data)
            if new_message:
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message_type = messenger.get_message_type(data)
                models.chats.insert_one(data)
                logging.info(
                    f"New Message; sender:{mobile} name:{name} type:{message_type}"
                )

        if 'statuses' in data['entry'][0]['changes'][0]['value']:
            messageId = data['entry'][0]['changes'][0]['value']['statuses'][0]['id']
            record = messenger.get_delivery(data)
            timestamp = data['entry'][0]['changes'][0]['value']['statuses'][0]['timestamp']
            if messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='text':
                        content = messenger.messages_store[messageId]['message_content']
                        new_messages = {
                            'messages': [{
                                 'id': messageId, 
                                 'timestamp': timestamp, 
                                 'text': {'body': content}, 
                                 'type': 'text'
                                 }]}
                        report = {record:timestamp}
                        data['entry'][0]['changes'][0]['value'].update(new_messages)
                        self.saveMessage(messageId=messageId, data=data, report=report)

            elif messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='image':
                imageId = messenger.messages_store[messageId]['message_content']
                report = {record:timestamp}
                new_messages = self.setMedia(contentId=messageId, timestamp=timestamp, heading='image', mediaType='image/jpeg', mediaId=imageId)
                data['entry'][0]['changes'][0]['value'].update(new_messages)
                self.saveMessage(messageId=messageId, data=data, report=report)
            
            elif messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='video':
                videoId = messenger.messages_store[messageId]['message_content']
                report = {record:timestamp}
                new_messages = self.setMedia(contentId=messageId, timestamp=timestamp, heading='video', mediaType='video/mp4', mediaId=videoId)
                data['entry'][0]['changes'][0]['value'].update(new_messages)
                self.saveMessage(messageId=messageId, data=data, report=report)
            
            elif messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='audio':
                audioId = messenger.messages_store[messageId]['message_content']
                report = {record:timestamp}
                new_messages = self.setMedia(contentId=messageId, timestamp=timestamp, heading='document', mediaType='audio/mpeg', mediaId=audioId)
                data['entry'][0]['changes'][0]['value'].update(new_messages)
                self.saveMessage(messageId=messageId, data=data, report=report)
            
            elif messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='document':
                documentId = messenger.messages_store[messageId]['message_content']
                report = {record:timestamp}
                new_messages = self.setMedia(contentId=messageId, timestamp=timestamp, heading='document', mediaType='application/pdf', mediaId=documentId)
                print(new_messages)
                data['entry'][0]['changes'][0]['value'].update(new_messages)
                self.saveMessage(messageId=messageId, data=data, report=report)

        response_message = 'Message received and stored successfully.'
        return Response({'status': 'success', 'message': response_message}, status=status.HTTP_201_CREATED)
    
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
        return Response({'msg': "success"}, status=status.HTTP_200_OK)
