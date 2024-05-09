from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authApp import renderers
from . import serializers
from rest_framework.permissions import IsAuthenticated
from authApp import models
import json

class AddMembers(APIView):
    renderer_classes = [renderers.UserRenderers]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = serializers.AddMemberSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Confirmation Link Sent...'}, status=status.HTTP_200_OK)
        
class AcceptInvitation(APIView):
    renderer_classes=[renderers.UserRenderers]
    permission_classes = [IsAuthenticated]
    def post(self, request, uid, token, format=None):
        serializer = serializers.AcceptInvitationSerializer(data=request.data, context={'uid': uid, 'token':token, 'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'User Added Successfully...'}, status=status.HTTP_200_OK)
        
class ChatUsers(APIView):
    renderer_classes=[renderers.UserRenderers]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        team_id = user.team.id
        members = models.User.objects.filter(team_id=team_id)
        serializer = serializers.ChatUsersSerializers(members, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)