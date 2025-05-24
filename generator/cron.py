
from django_cron import CronJobBase, Schedule
from .models import CustomUser
from django.utils import timezone

class ExpireUsersCron(CronJobBase):
    RUN_EVERY_MINS = 1440
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'generator.expire_users_cron'

    def do(self):
        for user in CustomUser.objects.filter(approved=True):
            if user.is_expired():
                user.approved = False
                user.save()
