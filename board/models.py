from django.db import models
from django.utils import timezone
from group.models import GroupMember


class Category(models.Model):
    name = models.CharField(max_length=100)


class Board(models.Model):
    group_member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=None, null=True)


class BoardComment(models.Model):
    content = models.TextField()
    group_member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=None, null=True)
