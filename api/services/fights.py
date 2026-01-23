from django.db import transaction
from api.models import Fight, Prediction
from api.services.predictions import score_prediction
from api.options import FightStatus


def complete_fight(fight, *, winner, method, round):
    if fight.status == FightStatus.STATUS_COMPLETED:
        raise ValueError("Fight already completed")

    with transaction.atomic():
        # Save or update result
        Fight.objects.update_or_create(
            fight=fight,
            defaults={
                "winner": winner,
                "method": method,
                "round": round,
            },
        )

        # Mark fight completed
        fight.status = FightStatus.STATUS_COMPLETED
        fight.save(update_fields=["status"])

        # Lock predictions to avoid race conditions
        predictions = Prediction.objects.select_for_update().filter(
            fight=fight,
            points_awarded__isnull=True,
        )

        for prediction in predictions:
            score_prediction(prediction)
