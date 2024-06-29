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
            response['messages'][0]['text'] = {
                'body': message
            }
            message_id = response['messages'][0]['id']
            messenger.set_message(message_id, message)
            
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendImage(APIView):
    def post(self, request):
        serializer = serializers.MediaSerializer(data=request.data)
        if serializer.is_valid():
            media = request.FILES['media']
            phone = request.data['phone']
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(media.name)[1]) as temp_file:
                for chunk in media.chunks():
                    temp_file.write(chunk)

            media_id = messenger.upload_media(
                media=temp_file.name
            )['id']
            response = messenger.send_image(
            image=media_id,
            recipient_id=phone,
            link=False
        )
            print(response)
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendVideo(APIView):
    def post(self, request):
        serializer = serializers.MediaSerializer(data=request.data)
        if serializer.is_valid():
            media = request.FILES['media']
            phone = request.data['phone']
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(media.name)[1]) as temp_file:
                for chunk in media.chunks():
                    temp_file.write(chunk)

            media_id = messenger.upload_media(
                media=temp_file.name
            )['id']
            response = messenger.send_video(
            video=media_id,
            recipient_id=phone,
            link=False
        )
            print(response)
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendPdf(APIView):
    def post(self, request):
        serializer = serializers.MediaSerializer(data=request.data)
        if serializer.is_valid():
            media = request.FILES['media']
            phone = request.data['phone']
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(media.name)[1]) as temp_file:
                for chunk in media.chunks():
                    temp_file.write(chunk)

            media_id = messenger.upload_media(
                media=temp_file.name
            )['id']
            response = messenger.send_document(
            document=media_id,
            recipient_id=phone,
            link=False
        )
            print(response)
            return Response({'msg': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class sendAudio(APIView):
    def post(self, request):
        serializer = serializers.MediaSerializer(data=request.data)
        if serializer.is_valid():
            media = request.FILES['media']
            phone = request.data['phone']
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(media.name)[1]) as temp_file:
                for chunk in media.chunks():
                    temp_file.write(chunk)

            media_id = messenger.upload_media(
                media=temp_file.name
            )['id']
            response = messenger.send_audio(
            audio=media_id,
            recipient_id=phone,
            link=False
        )
            print(response)
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
        changed_field = messenger.changed_field(data)

        if changed_field == "messages":
            new_message = messenger.get_mobile(data)
            if new_message:
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message_type = messenger.get_message_type(data)
                logging.info(
                    f"New Message; sender:{mobile} name:{name} type:{message_type}"
                )
                if message_type == "text":
                    message = messenger.get_message(data)
                    name = messenger.get_name(data)
                    logging.info("Message: %s", message)
                    messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

                elif message_type == "interactive":
                    message_response = messenger.get_interactive_response(data)
                    interactive_type = message_response.get("type")
                    message_id = message_response[interactive_type]["id"]
                    message_text = message_response[interactive_type]["title"]
                    logging.info(f"Interactive Message; {message_id}: {message_text}")

                elif message_type == "location":
                    message_location = messenger.get_location(data)
                    message_latitude = message_location["latitude"]
                    message_longitude = message_location["longitude"]
                    print(message_latitude, message_longitude, message_location)
                    logging.info("Location: %s, %s", message_latitude, message_longitude)

                elif message_type == "image":
                    image = messenger.get_image(data)
                    image_id, mime_type = image["id"], image["mime_type"]
                    image_url = messenger.query_media_url(image_id)
                    image_filename = messenger.download_media(image_url, mime_type)
                    print(image, image_id, image_url, image_filename)
                    print(f"{mobile} sent image {image_filename}")
                    logging.info(f"{mobile} sent image {image_filename}")

                elif message_type == "video":
                    video = messenger.get_video(data)
                    video_id, mime_type = video["id"], video["mime_type"]
                    video_url = messenger.query_media_url(video_id)
                    video_filename = messenger.download_media(video_url, mime_type)
                    print(f"{mobile} sent video {video_filename}")
                    logging.info(f"{mobile} sent video {video_filename}")

                elif message_type == "audio":
                    audio = messenger.get_audio(data)
                    audio_id, mime_type = audio["id"], audio["mime_type"]
                    audio_url = messenger.query_media_url(audio_id)
                    audio_filename = messenger.download_media(audio_url, mime_type)
                    print(f"{mobile} sent audio {audio_filename}")
                    logging.info(f"{mobile} sent audio {audio_filename}")

                elif message_type == "document":
                    file = messenger.get_document(data)
                    file_id, mime_type = file["id"], file["mime_type"]
                    file_url = messenger.query_media_url(file_id)
                    file_filename = messenger.download_media(file_url, mime_type)
                    print(f"{mobile} sent file {file_filename}")
                    logging.info(f"{mobile} sent file {file_filename}")
                else:
                    print(f"{mobile} sent {message_type} ")
                    print(data)
                    
            else:
                delivery = messenger.get_delivery(data)
                if delivery:
                    print(f"Message : {delivery}")
                else:
                    print("No new message")
    
        if 'statuses' in data['entry'][0]['changes'][0]['value']:
            messageId = data['entry'][0]['changes'][0]['value']['statuses'][0]['id']
            record = messenger.get_delivery(data)
            timestamp = data['entry'][0]['changes'][0]['value']['statuses'][0]['timestamp']
            if messageId in messenger.messages_store:
                        content = messenger.messages_store[messageId]
                        new_messages = {
                            'messages': [
                                {
                                 'id': messageId, 
                                 'timestamp': timestamp, 
                                 'text': {'body': content}, 
                                 'type': 'text'
                                 }
                                 ]}
                        report = {record:timestamp}
                        level = []
                        level.append(report)
                        data['entry'][0]['changes'][0]['value'].update(new_messages)
                        data['entry'][0]['changes'][0]['value']['level'] = level
                        query = {"entry.changes.value.messages.id": messageId}
                        document = models.chats.find_one(query)
                        if document:
                            models.chats.update_one(
                                query,
                                {"$push": {"entry.$[].changes.$[].value.level":level}}
                            )
                        else:
                            models.chats.insert_one(data)
                        print("sender delievery status", messenger.get_delivery(data))
                        success = {
                            messenger.get_delivery(data): timestamp
                        }
                        print(success)

        response_message = 'Message received and stored successfully.'
        return Response({'status': 'success', 'message': response_message}, status=status.HTTP_201_CREATED)