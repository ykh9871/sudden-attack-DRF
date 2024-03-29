from django.db import models
from django.utils import timezone
from user.models import User


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=None, null=True)


class GroupMember(models.Model):
    MEMBER = "M"
    ADMIN = "A"
    PENDING = "P"
    ROLE_CHOICES = [
        (MEMBER, "M"),
        (ADMIN, "A"),
        (PENDING, "P"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=None, null=True)
