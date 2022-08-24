from django.contrib.auth import get_user_model
from django.db import models


class InstagramData(models.Model):  # data for login and search in instagram
    username = models.CharField(max_length=20)
    sessionid = models.CharField(max_length=80, blank=False, null=False)

    active = models.BooleanField(default=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
