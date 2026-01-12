from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "avatar_url"]
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user

        if not user.is_staff:
            self.fields.pop("id", None)
            self.fields.pop("email", None)

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None


class UserSummarySerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "avatar_url"]

    def get_avatar_url(self, obj):
        return obj.avatar.url if obj.avatar else None
