from django.db import models
from api.options import Method


class Prediction(models.Model):
    user = models.ForeignKey("api.User", on_delete=models.CASCADE)
    fight = models.ForeignKey("api.Fight", on_delete=models.CASCADE)
    winner = models.ForeignKey("api.Fighter", on_delete=models.CASCADE)
    method = models.CharField(max_length=255, choices=Method.choices, null=True)
    round = models.IntegerField(null=True)
    date = models.DateField()
