from rest_framework.views import APIView
from rest_framework.response import Response
from . import renderers
from . import models
from authApp import models as authModel
from django.utils import timezone
import datetime
from rest_framework import status
from . import serializers
import requests, json

class indPhone(APIView):
    renderer_classes = [renderers.MessageRenderers]
    def post(self, request, format=None):
        serializer = serializers.indPhoneSerializer(data=request.data)
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
    def post(self, request):
        mobile_number = request.data['phone']
        AUTH_TOKEN = "EAAL7og371v4BOzH3qCP6o1o2WdIfdwZBU0M2Oy9xhqSK9IwJ1jQJjs1P69z3Kq9dchPdpuGc0MpL4Wna2XMxHFXivD4qPfDS1zZA7H7SY60H8IzmGh4wTFQ4H4Uz5SZAlCmYDiLZCRK3vDaRrUomNpiKFH6KfD2qTcnAceRRIZCFiUz3GOgVZBoMHl0ZAOXvz7mgAZDZD"
        try:
            url = "https://graph.facebook.com/v19.0/275772712289918/messages"
            headers = {
                "Authorization": f"Bearer {AUTH_TOKEN}",
                "Content-Type": "application/json"
            }
            data = {
                "messaging_product": "whatsapp",
                "to": mobile_number,
                "type": "template",
                "template": {
                    "name": "hello_world",
                    "language": {
                        "code": "en_US"
                    }
                }
            }
            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            return Response({'msg': response}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "Error comes..."}, status=status.HTTP_400_BAD_REQUEST)

class sendMessage(APIView):
    def post(self, request):
        mobile_number = request.data['phone']
        message = request.data['message']
        url = "https://graph.facebook.com/v19.0/275772712289918/messages"
        ACCESS_TOKEN = "EAAL7og371v4BOzH3qCP6o1o2WdIfdwZBU0M2Oy9xhqSK9IwJ1jQJjs1P69z3Kq9dchPdpuGc0MpL4Wna2XMxHFXivD4qPfDS1zZA7H7SY60H8IzmGh4wTFQ4H4Uz5SZAlCmYDiLZCRK3vDaRrUomNpiKFH6KfD2qTcnAceRRIZCFiUz3GOgVZBoMHl0ZAOXvz7mgAZDZD"
        try:
            payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": mobile_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
            })
            headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {ACCESS_TOKEN}'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            response_json = response.json()
            response_json['body'] = message
            print(response_json)
            phone_receiver = response_json['contacts'][0]['wa_id']
            sender = "91787853653"
            receiver = phone_receiver
            message_id = response_json['messages'][0]['id']
            message_type = "text"
            content = response_json['body']
            progress = ""
            print(sender, receiver)
            models.Message.objects.create(
                    sender=sender, 
                    receiver=receiver, 
                    message_id=message_id, 
                    message_type=message_type, 
                    content=content, 
                    status=progress, 
                )
            return Response({'msg': response_json, "db": "message stored success..."}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "Error comes..."}, status=status.HTTP_400_BAD_REQUEST)
        
        
class WebhookView(APIView):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))

        # Handle received messages
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            if 'text' in data['entry'][0]['changes'][0]['value']['messages']:
                try:
                    #Create a receiver's account
                    value = data['entry'][0]['changes'][0]['value']
                    phone_number = value['messages'][0]['from']
                    
                    #Message Saving
                    # ruser = authModel.User.objects.get(phone_id="275772712289918")
                    sender = phone_number
                    receiver = "91787853653"
                    message_id = value['messages'][0]['id']
                    message_type = value['messages'][0]['type']
                    content = value['messages'][0]['text']['body']
                    progress = "received"
                    timestamp = value['messages'][0]['timestamp']
                    timestamp_dt = datetime.datetime.fromtimestamp(int(timestamp), tz=datetime.timezone.utc)
                    models.Message.objects.create(
                        sender=sender, 
                        receiver=receiver, 
                        message_id=message_id, 
                        message_type=message_type, 
                        content=content, 
                        status=progress, 
                        timestamp= timestamp_dt
                    )

                    response_message = 'Message received and stored successfully.'

                    return Response({'status': 'success', 'message': response_message}, status=status.HTTP_201_CREATED)

                except KeyError as e:
                    return Response({'status': 'error', 'message': f'Missing key:'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({"msg": "Error comes..."}, status=status.HTTP_400_BAD_REQUEST)
            
            elif 'sticker' in data['entry'][0]['changes'][0]['value']['messages'][0]['type']:
                pass
            
        # Handle sent statuses
        elif 'statuses' in data['entry'][0]['changes'][0]['value']:
            try:
                print("webhook comes here....")
                value = data['entry'][0]['changes'][0]['value']
                status_data = value['statuses'][0]
                conversation_id = status_data['conversation']['id']
                w_sender = value['metadata']['display_phone_number']
                w_message_id = status_data['id']
                w_receiver = status_data['recipient_id']
                phone_id = value['metadata']['phone_number_id']
                expiration_timestamp = status_data['conversation']['expiration_timestamp']
                new_timestamp = datetime.datetime.fromtimestamp(int(expiration_timestamp), tz=datetime.timezone.utc)
                status_msg = status_data['status']

                # print(conversation_id, w_sender, w_message_id, w_receiver, expiration_timestamp, status_msg)

                conversation = models.Conversation.objects.get_or_create(
                    conversation_id=conversation_id, 
                    phone_id=phone_id,
                    sender = w_sender,
                    receiver = w_receiver,
                    expiration_timestamp = new_timestamp)[0]
                
                message = models.Message.objects.get(message_id=w_message_id)
                message.conversation = conversation
                message.status = status_msg
                message.save()

        #         conversation, created = Conversation.objects.get_or_create(
        #             conversation_id=conversation_id,
        #             defaults={'recipient_id': recipient_id}
        #         )

        #         message = Message.objects.create(
        #             message_id=message_id,
        #             conversation=conversation,
        #             from_number=recipient_id,
        #             status=status_msg,
        #             timestamp=datetime.datetime.fromtimestamp(int(timestamp), tz=timezone.utc),
        #         )

                response_message = 'Status received and stored successfully.'

                return Response({'status': 'success', 'message': response_message}, status=status.HTTP_201_CREATED)

            except KeyError as e:
                return Response({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'status': 'error', 'message': 'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)
        
