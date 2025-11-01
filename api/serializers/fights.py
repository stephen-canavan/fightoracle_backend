from rest_framework import serializers
from api.models import Fight
from api.serializers.fighters import FighterSummarySerializer
from api.serializers.events import EventSummarySerializer


class FightResultSerializer(serializers.ModelSerializer):
    winner = FighterSummarySerializer()
    method = serializers.CharField()
    round = serializers.IntegerField()

    class Meta:
        model = Fight
        fields = ["winner", "method", "round"]


class FightSerializer(serializers.ModelSerializer):
    fighter_red = FighterSummarySerializer()
    fighter_blue = FighterSummarySerializer()
    event = EventSummarySerializer()
    result = FightResultSerializer(source="*")

    class Meta:
        model = Fight
        fields = [
            "id",
            "event",
            "fighter_red",
            "fighter_blue",
            "weight_class",
            "scheduled_rounds",
            "title_fight",
            "result",
        ]


class FightSummarySerializer(FightSerializer):
    class Meta(FightSerializer.Meta):
        fields = [
            "id",
            "event",
            "fighter_red",
            "fighter_blue",
            "weight_class",
            "title_fight",
        ]
