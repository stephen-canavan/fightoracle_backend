from django.db import models
from api.options import Promotions


class Promotion(models.Model):
    name = models.CharField(max_length=255, choices=Promotions.choices, null=False)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"id: {self.id}, name: {self.name}"
