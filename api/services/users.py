from django.db import transaction


@transaction.atomic
def update_user_stats(prediction):
    from api.models import UserStats

    stats, _ = UserStats.objects.select_for_update().get_or_create(user=prediction.user)

    stats.total_predictions += 1
    stats.total_points += prediction.points_earned

    if not prediction.winner_correct:
        stats.save()
        return

    stats.winner_correct_count += 1

    if prediction.perfect_prediction:
        stats.perfect_prediction_count += 1

    elif prediction.method_correct:
        stats.winner_and_method_correct_count += 1

    elif prediction.round_correct:
        stats.winner_and_round_correct_count += 1

    if prediction.finish_correct:
        stats.winner_and_finish_correct_count += 1

    if prediction.decision_correct:
        stats.winner_and_decision_correct_count += 1

    stats.save()
