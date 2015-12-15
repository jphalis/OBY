from django.core.cache import cache
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

# from .models import Comment


# Add signals to apps.py in app folder
# https://docs.djangoproject.com/en/1.9/ref/applications/#application-configuration


@receiver(post_save, sender='comments.Comment')
def clear_cache(sender, instance, created, **kwargs):
    cache._cache.flush_all()


@receiver(pre_save, sender='comments.Comment')
def process_hashtags(sender, instance, **kwargs):
    html = []
    for word in instance.hashtag_field.value_to_string(instance).split():
        if word.startswith('#'):
            word = render_to_string('hashtags/_link.html',
                                    {'hashtag': word.lower()[1:]})

        html.append(word)
        instance.hashtag_enabled_text = ' '.join(html)
