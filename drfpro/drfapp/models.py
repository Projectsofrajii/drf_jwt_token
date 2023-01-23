from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):

    def create_user(self, username: str, first_name: str, email: str, password: str, is_staff=False,
                    is_superuser=False):

        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have an username')

        if not first_name:
            raise ValueError('Users must have an first_name')

        user = self.model(email=self.normalize_email(email))
        user.username = username
        user.first_name = first_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_superuser(self, username: str, first_name: str, email: str, password: str) -> "User":

        user = self.create_user(username=username, first_name=first_name, email=email, password=password, is_staff=True,
                                is_superuser=True)

        user.is_admin = True
        user.save()
        return user

class User(auth_models.AbstractUser):
    username = models.CharField(max_length=200,unique=True)
    first_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(null=True)
    is_admin = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    access_token = models.CharField(max_length=500, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_user']


