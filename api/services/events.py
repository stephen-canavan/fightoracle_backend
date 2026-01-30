from django.db import transaction
from api.models import Fight, Prediction
from api.options import EventStatus, FightStatus
from api.services.predictions import score_prediction


@transaction.atomic
def complete_event(event):
    from api.models import Event

    event = Event.objects.select_for_update().get(id=event)

    unfinished_fights = Fight.objects.filter(event=event).exclude(
        status__in=[
            FightStatus.COMPLETED,
            FightStatus.CANCELLED,
        ]
    )

    if unfinished_fights.exists():
        print(
            f"Attempted to complete event {event.title} with unfinished fights: {unfinished_fights}"
        )
        raise ValueError("Event cannot be completed; not all fights are finalized")

    predictions = Prediction.objects.filter(fight__event=event)
    for prediction in predictions:
        score_prediction(prediction)

    event.status = EventStatus.COMPLETED
    event.save(update_fields=["status"])
