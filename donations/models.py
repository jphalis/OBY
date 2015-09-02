from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Donation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    charge_id = models.CharField('Charge ID', max_length=100, help_text='The '
        'charge ID from Stripe.')
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    message = models.TextField(blank=True)

    def __unicode__(self):
        return '${0:.2f} - {}'.format(self.amount, self.charge_id)

    class Meta:
        ordering = ['-created']
