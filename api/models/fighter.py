from django.db import models
from api.options import WeightClass
from fightoracle_api import settings
from PIL import Image
from api.models.utils import sanitize_filename
import os


def fighter_image_upload_path(instance, filename):
    extension = filename.split(".")[-1]
    new_filename = f"{instance.fname}_{instance.sname}.{extension}"
    safe_filename = sanitize_filename(new_filename)
    return f"fighters/{instance.id}/{safe_filename}"


class Fighter(models.Model):
    fname = models.CharField(max_length=255)
    sname = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, null=True)
    promotion = models.ForeignKey("api.Promotion", on_delete=models.PROTECT)
    weight_class = models.CharField(max_length=255, choices=WeightClass.choices)
    dob = models.DateField()
    wins = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    draws = models.PositiveSmallIntegerField(default=0)
    no_contests = models.PositiveSmallIntegerField(default=0)
    dqs = models.PositiveSmallIntegerField(default=0)
    avatar = models.ImageField(
        upload_to=fighter_image_upload_path, null=True, blank=True
    )

    @property
    def name(self):
        return f"{self.fname} {self.sname}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            image_path = os.path.join(settings.MEDIA_ROOT, self.avatar.name)
            img = Image.open(image_path)

            # Resize image to max 512x512 for fighters
            max_size = (512, 512)
            img.thumbnail(max_size)
            img.save(image_path)

    def __str__(self):
        return f"id: {self.id}, name: {self.fname} {self.sname}"
