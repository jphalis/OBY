from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Newsletter


# Add signals to apps.py in app folder
# https://docs.djangoproject.com/en/1.9/ref/applications/#application-configuration


@receiver(post_save, sender=Newsletter)
def clear_cache(sender, instance, created, **kwargs):
    cache._cache.flush_all()
