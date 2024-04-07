from rest_framework import serializers
from .models import Category, Board, BoardComment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class BoardSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(source="group_member.group.id", read_only=True)
    group_member_id = serializers.IntegerField(source="group_member.id", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "group_id",
            "group_member_id",
            "category",
            "category_name",
            "title",
            "content",
            "created_at",
            "modified_at",
        ]
        read_only_fields = ["created_at", "modified_at"]


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["category", "title", "content"]


class BoardCommentSerializer(serializers.ModelSerializer):
    group_member_id = serializers.IntegerField(source="group_member.id", read_only=True)
    board_id = serializers.IntegerField(source="board.id", read_only=True)

    class Meta:
        model = BoardComment
        fields = [
            "id",
            "group_member_id",
            "board_id",
            "content",
            "created_at",
            "modified_at",
        ]
        read_only_fields = ["created_at", "modified_at"]


class BoardCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardComment
        fields = ["content"]
