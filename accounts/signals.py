from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

# from .models import Follower, MyUser


# Add signals to apps.py in app folder
# https://docs.djangoproject.com/en/1.9/ref/applications/#application-configuration


@receiver(post_save)
def clear_cache(sender, instance=None, created=False, **kwargs):
    list_of_models = ('Follower', 'MyUser')
    if sender.__name__ in list_of_models:
        if created:
            cache._cache.flush_all()
