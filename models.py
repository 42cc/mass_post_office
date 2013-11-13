from django.db import models

from django.contrib.auth.models import User


class SubscriptionSettings(models.Model):
    user = models.ForeignKey(User)
    subscribed = models.BooleanField(default=True)
