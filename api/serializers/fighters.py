from rest_framework import serializers
from api.models import Fighter


class FighterRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter
        fields = ["wins", "losses", "draws", "no_contests", "dqs"]


class FighterSerializer(serializers.ModelSerializer):
    record = FighterRecordSerializer(source="*")

    class Meta:
        model = Fighter
        fields = [
            "id",
            "fname",
            "sname",
            "nickname",
            "weight_class",
            "promotion",
            "dob",
            "record",
        ]


class FighterSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter
        fields = ["id", "name"]
