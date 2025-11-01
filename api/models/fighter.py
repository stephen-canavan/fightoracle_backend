from django.db import models
from api.options import WeightClass


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

    @property
    def name(self):
        return f"{self.fname} {self.sname}"

    def __str__(self):
        return f"id: {self.id}, name: {self.fname} {self.sname}"
