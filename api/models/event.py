from django.db import models
from api.options import EventStatus


class Event(models.Model):
    name = models.CharField(max_length=255)
    promotion = models.ForeignKey("api.Promotion", on_delete=models.PROTECT)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=EventStatus.choices, default=EventStatus.SCHEDULED
    )
    date = models.DateTimeField()

    def __str__(self):
        return f"id: {self.id},promotion: {self.promotion}, name: {self.name}, date: {self.date}"
