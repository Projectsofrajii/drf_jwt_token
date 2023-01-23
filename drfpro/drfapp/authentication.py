import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework_simplejwt import exceptions

from . import models

class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            return None

        try:
            payload = jwt.decode(token,settings.JWT_SECRET,algorithms=["HS256"])
        except:
            raise exceptions.AuthenticationFailed("unauthorized")

        user = models.User.objects.filter(email=payload["email"]).first()
        return (user,None)