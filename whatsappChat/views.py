from rest_framework.views import APIView
from rest_framework.response import Response
from . import renderers
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
            print(response.text)
            return Response({'msg': response}, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "Error comes..."}, status=status.HTTP_400_BAD_REQUEST)
        
