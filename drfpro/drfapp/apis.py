from django.contrib.auth import login
from rest_framework import views, response, exceptions, permissions, status
from rest_framework.response import Response

from .models import User
from .import serializers as user_serializer
from .import services,authentication

class RegisterApi(views.APIView):
    def post(self,request):
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        serializer.instance = services.create_user(user_dc=data)
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)

class LoginApi(views.APIView):
    def post(self,request):
        email = request.data["email"]
        password = request.data["password"]
        user = services.user_email_selector(email=email)
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credential")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Password not matched")
        token = services.create_token(email=user.email)
        resp = response.Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)
        User.objects.filter(email=email).update(access_token=token)
        return resp

class UserApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        user = request.user
        serializer = user_serializer.UserSerializer(user)
        return response.Response(serializer.data)

class LogoutApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "Logout Successfully.."}
        return resp

'''eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNjc0NTM3NDM3LCJpYXQiOjE2NzQ0NTEwMzd9.nKzwxiF4J3NXs50XxR_Y9f5xdsdVwQ5fPQTLfxPKCr8
'''