from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from api.models.utils import user_image_upload_path
from PIL import Image
import os
from fightoracle_api import settings


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=user_image_upload_path, null=True, blank=True)

    USERNAME_FIELD = "username"
    lookup_field = "username"

    def __str__(self):
        return f"id: {self.id}, username: {self.username}, email: {self.email}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            image_path = os.path.join(settings.MEDIA_ROOT, self.avatar.name)
            img = Image.open(image_path)

            # Resize image to max 512x512 for fighters
            max_size = (512, 512)
            img.thumbnail(max_size)
            img.save(image_path)
