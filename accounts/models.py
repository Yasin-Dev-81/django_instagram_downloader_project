from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return "%s with %s year old" % (self.username, self.age)

    def get_absolute_url(self):
        return reverse('home_url', args=[self.pk, ])


class TelegramUsers(models.Model):
    username = models.CharField(max_length=32, blank=False, null=False)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=64)

    user_id = models.CharField(max_length=10)
    chat_id = models.CharField(max_length=10)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    joined_to_chanel = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)

    def __str__(self):
        return "{username} with {user_id}".format(username=self.username, user_id=self.user_id)
