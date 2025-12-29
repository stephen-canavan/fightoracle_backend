from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, validators=[validate_password])
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = "username"
    lookup_field = "username"

    def __str__(self):
        return f"id: {self.id}, username: {self.username}, email: {self.email}"
