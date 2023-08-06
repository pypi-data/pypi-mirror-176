from .enums import LokGrantType
from django.db import models  # Create your models here.
from django.contrib.auth.models import AbstractUser


class LokUser(AbstractUser):
    """A reflection on the real User"""
    sub = models.CharField(max_length=1000, null=True, blank=True)
    iss = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        permissions = [("imitate", "Can imitate me")]



class LokApp(models.Model):
    identifier = models.CharField(max_length=2000)
    version = models.CharField(max_length=2000)

    class Meta:
        unique_together = ("identifier", "version")


class LokClient(models.Model):
    iss = models.CharField(max_length=2000)
    client_id = models.CharField(unique=True, max_length=2000)
    name = models.CharField(max_length=2000)
    app = models.ForeignKey(LokApp, on_delete=models.CASCADE)
    grant_type = models.CharField(choices=LokGrantType.choices, max_length=2000)

    class Meta:
        unique_together = ("iss", "client_id")

    def __str__(self):
        return f"{self.name}"
