from django.db import models
from api.options import WeightClass, Method


class Fight(models.Model):
    event = models.ForeignKey("api.Event", on_delete=models.PROTECT)
    fighter_red = models.ForeignKey(
        "api.Fighter", related_name="red_corner", on_delete=models.PROTECT
    )
    fighter_blue = models.ForeignKey(
        "api.Fighter", related_name="blue_corner", on_delete=models.PROTECT
    )
    weight_class = models.CharField(max_length=255, choices=WeightClass.choices)
    scheduled_rounds = models.PositiveSmallIntegerField(default=3)
    title_fight = models.BooleanField()

    # Result
    winner = models.ForeignKey("api.Fighter", null=True, on_delete=models.PROTECT)
    method = models.CharField(max_length=255, choices=Method.choices)
    round = models.IntegerField()

    def __str__(self):
        return f"{self.fighter_red.name} vs {self.fighter_blue.name}"
