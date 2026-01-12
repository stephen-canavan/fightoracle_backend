from django.db import models
from api.options import Promotions
from api.models.utils import promotion_image_upload_path
from PIL import Image
import os
from fightoracle_api import settings


class Promotion(models.Model):
    name = models.CharField(max_length=255, choices=Promotions.choices, null=False)
    country = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to=promotion_image_upload_path, null=True, blank=True
    )

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.logo:
            image_path = os.path.join(settings.MEDIA_ROOT, self.logo.name)
            img = Image.open(image_path)

            # Resize image to max 512x512 for fighters
            max_size = (512, 512)
            img.thumbnail(max_size)
            img.save(image_path)
