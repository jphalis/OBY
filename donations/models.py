from django.conf import settings
from django.db import models

from decimal import Decimal

from core.models import TimeStampedModel

# Create your models here.


class Donation(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    donation_id = models.CharField(max_length=30, default="ABC", unique=True)
    amount = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    name = models.CharField(max_length=80)
    email = models.EmailField(verbose_name='email', max_length=80)
    message = models.CharField(max_length=4000, null=True, blank=True)

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
