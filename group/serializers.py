from rest_framework import serializers
from .models import Group, GroupMember
from user.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "description", "created_at", "member_count"]


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "description"]

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        GroupMember.objects.create(
            user=self.context["request"].user, group=group, role="ADMIN"
        )
        return group


class GroupMembershipRequestSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source="group.name")

    class Meta:
        model = GroupMember
        fields = ["group_name", "created_at"]


class MemberRequestsViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    nickname = serializers.CharField(source="user.nickname")
    occupation_name = serializers.CharField(source="user.occupation.name")

    class Meta:
        model = GroupMember
        fields = ["id", "username", "nickname", "occupation_name", "created_at"]


class AdminUserSerializer(serializers.Serializer):
    role = serializers.CharField()
    group_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
