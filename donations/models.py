from django.conf import settings
from django.db import models

from decimal import Decimal

# Create your models here.


STATUS_CHOICES = (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)


class Donation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order_id = models.CharField(max_length=30, default="ABC", unique=True)
    amount = models.DecimalField(default=0.00, max_digits=1000,
                                 decimal_places=2)
    name = models.CharField(max_length=80)
    email = models.EmailField(verbose_name='email', max_length=80)
    message = models.CharField(max_length=4000, null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,
                              default="Started")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.order_id

    class Meta:
        app_label = 'donations'
        ordering = ['-updated', '-timestamp']

    def get_total_amount(self):
        instance = Donation.objects.get(id=self.id)
        two_places = Decimal(10) ** -2
        total_dec = Decimal(self.amount).quantize(two_places)
        instance.amount = total_dec
        instance.save()
        return instance.amount
