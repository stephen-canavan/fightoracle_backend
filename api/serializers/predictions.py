from api.models import Prediction
from rest_framework import serializers
from api.serializers.events import EventSummarySerializer
from api.serializers.users import UserSummarySerializer
from api.serializers.fights import FightSummarySerializer, FightResultSerializer
from api.serializers.fighters import FighterSummarySerializer


class PredictionResultSerializer(serializers.ModelSerializer):
    winner = FighterSummarySerializer()

    class Meta:
        model = Prediction
        fields = ["winner", "method", "round"]


class PredictionSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer()
    fight = FightSummarySerializer()
    event = EventSummarySerializer(source="fight.event")
    result = FightResultSerializer(source="fight")
    predicted_result = PredictionResultSerializer(source="*")

    class Meta:
        model = Prediction
        fields = [
            "id",
            "user",
            "event",
            "fight",
            "predicted_result",
            "result",
            "date",
        ]
