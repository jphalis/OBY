from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MyUser


@receiver(post_save, sender=MyUser)
def clear_cache(sender, instance, created, **kwargs):
    cache.clear()
