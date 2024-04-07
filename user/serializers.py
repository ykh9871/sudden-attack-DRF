from rest_framework import serializers
from .models import User, Occupation


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    occupation = serializers.PrimaryKeyRelatedField(queryset=Occupation.objects.all())

    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "email",
            "password",
            "occupation",
            "refresh_token",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    occupation_name = serializers.CharField(source="occupation.name")

    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "email",
            "occupation_name",
            "created_at",
            "modified_at",
        ]
