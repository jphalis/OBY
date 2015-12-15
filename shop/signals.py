from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.utils import timezone

from .models import Product


timeframe_dates_update = Signal(providing_args=['new_date_start'])

listuse_status_check = Signal()

use_dates_update = Signal()


def update_listuse_status(sender, **kwargs):
    product = sender
    current_date = timezone.now()

    if product.list_date_start > current_date:
        product.listed = False
    elif product.list_date_start <= current_date and product.list_date_end >= current_date:
        product.listed = True
    elif product.list_date_start <= current_date and product.list_date_end < current_date:
        product.listed = False
    else:
        pass

    if product.buyers.count() == product.max_downloads:
        product.listed = False
    else:
        pass

    if product.use_date_end >= current_date:
        product.useable = True
    elif product.use_date_end < current_date:
        product.useable = False
    else:
        pass

    product.save()

listuse_status_check.connect(update_listuse_status)


@receiver(post_save, sender=Product)
def delete_buyers_cache(sender, instance, created, **kwargs):
    try:
        del sender.get_buyer_usernames
    except AttributeError:
        pass


@receiver(post_save, sender=Product)
def clear_cache(sender, instance, created, **kwargs):
    cache._cache.flush_all()
