from rest_framework import serializers
from api.models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["id", "name", "country"]


class PromotionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["id", "name"]
