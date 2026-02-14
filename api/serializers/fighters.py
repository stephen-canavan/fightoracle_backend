from rest_framework import serializers
from api.models import Fighter
from api.serializers.promotions import PromotionSummarySerializer
from fightoracle_api.settings import COUNTRIES


class FighterRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fighter
        fields = ["wins", "losses", "draws", "no_contests", "dqs"]


class FighterSerializer(serializers.ModelSerializer):
    record = FighterRecordSerializer(source="*")
    promotion = PromotionSummarySerializer()
    avatar_url = serializers.ImageField(source="avatar")
    country = serializers.SerializerMethodField()

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
            "height",
            "reach",
            "record",
            "avatar_url",
            "country",
        ]

    def get_country(self, obj):
        if not obj.country:
            return None

        flag_url = COUNTRIES.get_flag(obj.country.code)

        return {
            "code": obj.country.code,
            "name": obj.country.name,
            "flag": flag_url,  # CDN flag URL
        }


class FighterSummarySerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(source="avatar")

    class Meta:
        model = Fighter
        fields = ["id", "name", "avatar_url"]
