from django.db import models


class UserStats(models.Model):
    user = models.OneToOneField(
        "api.User", on_delete=models.CASCADE, primary_key=True, related_name="stats"
    )

    total_predictions = models.IntegerField(default=0)

    winner_correct_count = models.IntegerField(default=0)
    perfect_prediction_count = models.IntegerField(default=0)
    winner_and_decision_correct_count = models.IntegerField(default=0)
    winner_and_finish_correct_count = models.IntegerField(default=0)
    winner_and_method_correct_count = models.IntegerField(default=0)
    winner_and_round_correct_count = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    @property
    def prediction_accuracy(self):
        if self.total_predictions == 0:
            return 0
        return (self.winner_correct_count / self.total_predictions) * 100
