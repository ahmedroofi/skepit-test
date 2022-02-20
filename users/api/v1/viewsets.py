from rest_framework import viewsets, permissions

from common.custom_response import spkt_response
from .serializers import *


class UserRegister(viewsets.ViewSet):

    def create(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_dict = UserSerializer(user).data
        return spkt_response(user_dict)


class UserLogin(viewsets.ViewSet):

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_dict = UserSerializer(user).data
        return spkt_response(user_dict)


class Logout(viewsets.ViewSet):

    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, format=None):
        request.user.auth_token.delete()
        return spkt_response("Logged Out")
