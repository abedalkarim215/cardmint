
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CustomUser(AbstractUser):
    SUBSCRIPTIONS = [
        ('7', 'أسبوع'),
        ('30', 'شهر'),
        ('365', 'سنة')
    ]
    subscription = models.CharField(max_length=3, choices=SUBSCRIPTIONS)
    approved = models.BooleanField(default=False)
    subscribed_on = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        if not self.subscribed_on:
            return True
        return timezone.now() > self.subscribed_on + timedelta(days=int(self.subscription))
