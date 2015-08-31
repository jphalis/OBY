from django.conf import settings
from django.db import models

from core.models import TimeStampedModel

# Create your models here.


class Newsletter(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    subscribed = models.BooleanField(default=True)

    class Meta:
        app_label = 'newsletter'

    def __unicode__(self):
        if self.subscribed:
            return "Subscribed"
        else:
            return "Unsubscribed"

    def email(self):
        return "{}".format(self.user.email)
