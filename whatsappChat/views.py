from rest_framework.views import APIView
from rest_framework.response import Response
from . import renderers
from rest_framework import status
from . import serializers
import requests

# Create your views here.
class indPhone(APIView):
    renderer_classes = [renderers.MessageRenderers]
    def post(self, request, format=None):
        serializer = serializers.indPhoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class sendMsg(APIView):
    def post(self, request):
        mobile_number = request.data['phone']
        url = "https://graph.facebook.com/v19.0/293632593827326/messages"
        headers = {
            "Authorization": "Bearer EAAL7og371v4BOZBtKG2MiPiI6eSxtt06tC69MjxUxkWiwX1o2bs4Qh7ZAv4pLJQxMJHm5txyggAArBL1pMNm2GeGMlyAeQYeP3qC63O6bZBFHdal3uBsTTdJhZClB3lu4sQdjet0QkU8ksU1thNBmEW36eO1vzk6wmkQ7GbxaAZAFTYwQ1cduW9fMHqveBGfio2ELGNru08gU2ajckgcZD",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": "91"+mobile_number,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {
                    "code": "en_US"
                }
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        return Response({'msg': response}, status=status.HTTP_200_OK)