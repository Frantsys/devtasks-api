from rest_framework import serializers

from apps.users.serializers import UserReadSerializer
from .models import Team, TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    user_detail = UserReadSerializer(source="user", read_only=True)

    class Meta:
        model = TeamMember
        fields = [
            "id", "user", "user_detail", "team", "role",
            "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "is_deleted", "created_at", "updated_at", "user_detail"]


class TeamMemberInlineSerializer(serializers.ModelSerializer):
    user_detail = UserReadSerializer(source="user", read_only=True)

    class Meta:
        model = TeamMember
        fields = ["id", "user", "user_detail", "role"]
        read_only_fields = ["id", "user_detail"]


class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberInlineSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            "id", "sector", "member_count", "members",
            "is_deleted", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "is_deleted", "created_at", "updated_at", "members", "member_count"]

    def get_member_count(self, obj) -> int:
        return obj.members.filter(is_deleted=False).count()


class TeamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "sector", "is_deleted", "created_at", "updated_at"]
        read_only_fields = ["id", "is_deleted", "created_at", "updated_at"]
