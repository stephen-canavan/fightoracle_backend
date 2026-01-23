from django.db import models
from api.options import Method
from api.services.predictions import calculate_potential_points


class Prediction(models.Model):
    user = models.ForeignKey("api.User", on_delete=models.CASCADE)
    event = models.ForeignKey("api.Event", on_delete=models.PROTECT)
    fight = models.ForeignKey("api.Fight", on_delete=models.CASCADE)
    prediction_date = models.DateField()

    # Prediction details
    predicted_winner = models.ForeignKey("api.Fighter", on_delete=models.PROTECT)
    predicted_method = models.CharField(
        max_length=255, choices=Method.choices, blank=True, null=True
    )
    predicted_round = models.IntegerField(blank=True, null=True)  # restrict to 1 - 5

    # Results
    winner_correct = models.BooleanField(null=True)
    method_correct = models.BooleanField(null=True)
    round_correct = models.BooleanField(null=True)

    points_potential = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "fight"],
                name="one_prediction_per_user_per_fight",
            )
        ]

    def save(self, *args, **kwargs):
        self.points_potential = calculate_potential_points(self)

        update_fields = kwargs.get("update_fields")
        if update_fields:
            kwargs["update_fields"] = set(update_fields) | {"points_potential"}

        super().save(*args, **kwargs)
