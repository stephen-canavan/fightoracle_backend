from django.utils import timezone

WINNER_POINTS = 5
METHOD_POINTS = 3
ROUND_POINTS = 2


def calculate_total_points(prediction):
    total = 0
    if prediction.winner_correct:
        total += WINNER_POINTS
    if prediction.method_correct:
        total += METHOD_POINTS
    if prediction.round_correct:
        total += ROUND_POINTS
    return total


def calculate_potential_points(prediction):
    if prediction.predicted_winner is None:
        return 0  # No points if winner not known yet
    total = WINNER_POINTS
    if prediction.predicted_method is not None:
        total += METHOD_POINTS
    if prediction.predicted_round is not None:
        total += ROUND_POINTS
    return total


def score_prediction(prediction):
    fight = prediction.fight

    winner_correct = prediction.predicted_winner == fight.winner
    method_correct = prediction.predicted_method == fight.method
    round_correct = prediction.predicted_round == fight.round

    points = calculate_total_points(prediction)

    prediction.winner_correct = winner_correct
    prediction.method_correct = method_correct
    prediction.round_correct = round_correct
    prediction.points_earned = points

    prediction.save(
        update_fields=[
            "winner_correct",
            "method_correct",
            "round_correct",
            "points_earned",
            "potential_points",
        ]
    )
