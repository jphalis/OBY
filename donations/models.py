from django.conf import settings
from django.db import models

from decimal import Decimal

from core.models import TimeStampedModel

# Create your models here.


class Donation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    charge_id = models.CharField('Charge ID', max_length=100, help_text='The '
        'charge ID from Stripe.')
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    message = models.TextField(blank=True)

    def __unicode__(self):
        return self.donation_id

    class Meta:
        app_label = 'donations'
        ordering = ['-modified', '-created']

    def get_total_amount(self):
        instance = Donation.objects.get(id=self.id)
        two_places = Decimal(10) ** -2
        total_dec = Decimal(self.amount).quantize(two_places)
        instance.amount = total_dec
        instance.save()
        return instance.amount
