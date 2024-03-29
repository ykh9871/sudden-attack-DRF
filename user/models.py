from django.db import models
from django.utils import timezone


class Occupation(models.Model):
    name = models.CharField(max_length=100, unique=True)


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=None, null=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    refresh_token = models.CharField(max_length=255, default=None, null=True)
    active = models.IntegerField(default=1)
