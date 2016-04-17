from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User)
    permissions = models.ManyToManyField("Permission")

    class Meta:
        ordering = ("-id",)
        abstract = True


class Administrator(Account):
    pass


class DNSUser(Account):
    pass


class Permission(models.Model):
    name = models.CharField(max_length=50)
