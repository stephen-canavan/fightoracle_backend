from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255)
    promotion = models.ForeignKey("api.Promotion", on_delete=models.PROTECT)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return (f"id: {self.id},promotion: {self.promotion}, name: {self.name}, date: {self.date}")