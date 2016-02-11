from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from accounts.models import Advertiser
from core.models import TimeStampedModel

# Create your models here.


def upload_location(instance, filename):
    return "{}/products/{}".format(instance.owner.username, filename)


class ProductManager(models.Manager):
    def featured(self, obj):
        return super(ProductManager, self).get_queryset() \
            .filter(is_featured=True) \
            .select_related('owner') \
            .prefetch_related('buyers')

    def listed(self, obj):
        return super(ProductManager, self).get_queryset() \
            .filter(is_listed=True) \
            .select_related('owner') \
            .prefetch_related('buyers')

    def useable(self, obj):
        return super(ProductManager, self).get_queryset() \
            .filter(is_useable=True) \
            .select_related('owner') \
            .prefetch_related('buyers')

    def redeemed_by_user(self, user):
        return super(ProductManager, self).get_queryset() \
            .filter(buyers=user) \
            .select_related('owner') \
            .prefetch_related('buyers')


class Product(TimeStampedModel):
    owner = models.ForeignKey(Advertiser)
    buyers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='buyers', blank=True)
    is_listed = models.BooleanField(default=False)
    is_useable = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    title = models.CharField(max_length=120, null=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    cost = models.DecimalField(decimal_places=0, max_digits=10, default=10)
    discount_cost = models.DecimalField(decimal_places=0, max_digits=8,
                                        null=True, blank=True)
    max_downloads = models.PositiveIntegerField(null=True, blank=True)
    promo_code = models.CharField(max_length=30)
    list_date_start = models.DateTimeField(verbose_name='Listing Start Date',
                                           null=True)
    list_date_end = models.DateTimeField(verbose_name='Listing Expiration',
                                         null=True)
    use_date_start = models.DateTimeField(verbose_name='Usage Start Date',
                                          null=True)
    use_date_end = models.DateTimeField(verbose_name='Usage Expiration',
                                        null=True)

    objects = ProductManager()

    class Meta:
        ordering = ('list_date_end',)
        app_label = 'shop'

    def __unicode__(self):
        return u"{}".format(self.owner)

    @cached_property
    def get_buyer_usernames(self):
        return map(str, self.buyers.all().values_list('username', flat=True))

    @cached_property
    def get_buyers_info(self):
        return self.buyers.values(
            'username', 'full_name', 'profile_picture')

    @property
    def get_image_url(self):
        if self.image:
            return "{}{}".format(settings.MEDIA_URL, self.image)
        else:
            # Change this to a product-looking image
            return settings.STATIC_URL + 'img/default_profile_picture.jpg'
