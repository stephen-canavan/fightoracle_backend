from rest_framework import serializers
from api.models import Fight, Fighter
from api.serializers.fighters import FighterSummarySerializer
from api.serializers.events import EventSummarySerializer


class FightResultSerializer(serializers.ModelSerializer):
    winner = FighterSummarySerializer()
    winning_method = serializers.CharField()
    winning_round = serializers.IntegerField()

    class Meta:
        model = Fight
        fields = ["winner", "winning_method", "winning_round"]


class FightFighterSummarySerializer(serializers.ModelSerializer):
    # 'record' will be pulled from the Fight instance via 'source'
    record = serializers.JSONField(source="fighter_record")

    class Meta:
        model = Fighter
        fields = ["id", "name", "record"]


class FightSerializer(serializers.ModelSerializer):
    fighter_red = FightFighterSummarySerializer(source="get_fighter_red_with_record")
    fighter_blue = FightFighterSummarySerializer(source="get_fighter_blue_with_record")
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
            "is_title_fight",
            "is_main_event",
            "status",
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
            "is_title_fight",
            "is_main_event",
        ]
