from django.contrib.auth import get_user_model
from django.db import models


class ActivesManager(models.Manager):
    def get_queryset(self):
        return super(ActivesManager, self).get_queryset().filter(active=True)


class InstagramData(models.Model):  # data for login and search in instagram
    username = models.CharField(max_length=20)
    sessionid = models.CharField(max_length=80, blank=False, null=False)

    active = models.BooleanField(default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    # manager
    object = models.Manager()
    actives_manager = ActivesManager()

    def __str__(self):
        return self.username
