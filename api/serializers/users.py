from rest_framework import serializers
from api.models import User, UserStats


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = [
            "total_predictions",
            "winner_correct_count",
            "perfect_prediction_count",
            "winner_and_decision_correct_count",
            "winner_and_finish_correct_count",
            "winner_and_method_correct_count",
            "winner_and_round_correct_count",
            "total_points",
            "prediction_accuracy",
        ]


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "avatar_url", "stats"]
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user

        if not user.is_staff:
            self.fields.pop("id", None)
            self.fields.pop("email", None)

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None

    def get_stats(self, user):
        stats, _ = UserStats.objects.get_or_create(user=user)
        return UserStatsSerializer(stats).data


class UserSummarySerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    stats = UserStatsSerializer(source="*", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "avatar_url", "stats"]

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None
