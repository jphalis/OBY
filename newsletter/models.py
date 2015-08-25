from django.conf import settings
from django.db import models

# Create your models here.


class Newsletter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    subscribed = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'newsletter'

    def __unicode__(self):
        if self.subscribed:
            return "Subscribed"
        else:
            return "Unsubscribed"

    def email(self):
        return "{}".format(self.user.email)
