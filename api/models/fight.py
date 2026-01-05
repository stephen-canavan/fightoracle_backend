from django.db import models
from api.options import FightStatus, WeightClass, Method


class Fight(models.Model):
    event = models.ForeignKey("api.Event", on_delete=models.PROTECT)
    fighter_red = models.ForeignKey(
        "api.Fighter", related_name="red_corner", on_delete=models.PROTECT
    )
    fighter_blue = models.ForeignKey(
        "api.Fighter", related_name="blue_corner", on_delete=models.PROTECT
    )
    fighter_red_record = models.CharField(max_length=50, blank=True, null=True)
    fighter_blue_record = models.CharField(max_length=50, blank=True, null=True)
    weight_class = models.CharField(max_length=255, choices=WeightClass.choices)
    scheduled_rounds = models.PositiveSmallIntegerField(default=3)
    is_title_fight = models.BooleanField(default=False)
    is_main_event = models.BooleanField(default=False)
    status = models.CharField(
        max_length=255, choices=FightStatus.choices, default=FightStatus.SCHEDULED
    )

    # Result
    winner = models.ForeignKey(
        "api.Fighter", blank=True, null=True, on_delete=models.PROTECT
    )
    winning_method = models.CharField(
        max_length=255, choices=Method.choices, blank=True, null=True
    )
    winning_round = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.fighter_red.name} vs {self.fighter_blue.name}"
