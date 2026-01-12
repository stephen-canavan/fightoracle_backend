from rest_framework import serializers
from api.models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    logo_url = serializers.ImageField(source="logo")

    class Meta:
        model = Promotion
        fields = ["id", "name", "country", "logo_url"]


class PromotionSummarySerializer(serializers.ModelSerializer):
    logo_url = serializers.ImageField(source="logo")

    class Meta:
        model = Promotion
        fields = ["id", "name", "logo_url"]
