from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def clear_cache(sender, instance, created, **kwargs):
    cache._cache.flush_all()
