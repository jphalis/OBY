from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Donation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    charge_id = models.CharField('Charge ID', max_length=100, help_text='The '
        'charge ID from Stripe.', blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    message = models.TextField(max_length=2000, blank=True)
    is_anonymous = models.BooleanField(default=True)

    def __unicode__(self):
        return '{:.2f}'.format(self.amount)

    class Meta:
        ordering = ['-created']
