from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from .models import Category, Board, BoardComment, GroupMember
from .serializers import (
    CategorySerializer,
    BoardSerializer,
    BoardCreateSerializer,
    BoardCommentSerializer,
    BoardCommentCreateSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BoardListView(generics.ListAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs["group_id"]
        return Board.objects.filter(group_member__group_id=group_id)


class BoardCreateView(generics.CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group_id = self.kwargs["group_id"]
        try:
            group_member = GroupMember.objects.get(
                group_id=group_id, user=self.request.user
            )
            serializer.save(group_member=group_member)
        except GroupMember.DoesNotExist:
            raise PermissionDenied("You are not a member of this group.")


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        board = self.get_object()
        group_member = board.group_member
        if group_member.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this board.")
        serializer.save(modified_at=timezone.now())

    def perform_destroy(self, instance):
        group_member = instance.group_member
        if group_member.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this board.")
        instance.delete()


class BoardCommentListView(generics.ListAPIView):
    serializer_class = BoardCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs["board_id"]
        return BoardComment.objects.filter(board_id=board_id)


class BoardCommentCreateView(generics.CreateAPIView):
    serializer_class = BoardCommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        board_id = self.kwargs["board_id"]
        try:
            board = Board.objects.get(id=board_id)
            group_member = GroupMember.objects.get(
                group=board.group_member.group, user=self.request.user
            )
            serializer.save(group_member=group_member, board=board)
        except GroupMember.DoesNotExist:
            raise PermissionDenied(
                "You are not a member of the group associated with this board."
            )


class BoardCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardComment.objects.all()
    serializer_class = BoardCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        comment = self.get_object()
        group_member = comment.group_member
        if group_member.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this comment.")
        serializer.save(modified_at=timezone.now())

    def perform_destroy(self, instance):
        group_member = instance.group_member
        if group_member.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()
