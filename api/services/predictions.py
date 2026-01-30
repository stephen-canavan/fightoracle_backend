from api.services.users import update_user_stats
from api.options import Method

WINNER_POINTS = 8
FINISH_POINTS = 3
METHOD_POINTS = 4
ROUND_POINTS = 3
PERFECT_BONUS_POINTS = 1


def calculate_total_points(prediction):
    total = 0
    if prediction.winner_correct:
        total += WINNER_POINTS
    if prediction.finish_correct:
        total += FINISH_POINTS
        return total
    if prediction.method_correct:
        total += METHOD_POINTS
    if prediction.round_correct:
        total += ROUND_POINTS
    if prediction.perfect_prediction:
        total += PERFECT_BONUS_POINTS
    return total


def calculate_potential_points(prediction):
    total = 0

    if not prediction.predicted_winner:
        return total  # No points if winner not known yet

    total += WINNER_POINTS

    # If only FINISH is predicted, not eligible for other points
    if prediction.predicted_method == Method.FINISH:
        total += FINISH_POINTS
        return total

    if prediction.predicted_method:
        total += METHOD_POINTS
    if prediction.predicted_round and prediction.predicted_method != Method.DEC:
        total += ROUND_POINTS
    if prediction.method_correct and prediction.round_correct:
        total += PERFECT_BONUS_POINTS
    return total


def score_prediction(prediction):
    fight = prediction.fight

    prediction.winner_correct = prediction.predicted_winner == fight.winner
    prediction.decision_correct = (
        prediction.predicted_method == Method.DEC and fight.winning_method == Method.DEC
    )
    prediction.method_correct = prediction.predicted_method == fight.winning_method
    prediction.finish_correct = (
        prediction.predicted_method == Method.FINISH
        and fight.winning_method in [Method.KO, Method.KOTKO, Method.SUB]
    )
    prediction.round_correct = prediction.predicted_round == fight.winning_round

    prediction.perfect_prediction = (
        prediction.winner_correct
        and (prediction.method_correct and prediction.round_correct)
        or prediction.decision_correct
    )

    points = calculate_total_points(prediction)

    prediction.points_earned = points

    prediction.save(
        update_fields=[
            "winner_correct",
            "method_correct",
            "round_correct",
            "finish_correct",
            "points_earned",
            "points_potential",
            "perfect_prediction",
        ]
    )

    update_user_stats(prediction)
