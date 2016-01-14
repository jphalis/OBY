from django.conf import settings
from django.db import models

from core.models import TimeStampedModel
from photos.models import Photo


class Flag(TimeStampedModel):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ForeignKey(Photo)
    comment = models.TextField(null=True, blank=True)
    resolved = models.BooleanField(default=False)
    flag_count = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'flag'
