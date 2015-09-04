from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from .models import PageView


page_view = Signal(providing_args=[
                   'page_path',
                   'primary_obj',
                   'secondary_obj'])


def page_view_received(sender, **kwargs):
    kwargs.pop('signal', None)
    page_path = kwargs.pop('page_path')
    primary_obj = kwargs.pop('primary_obj', None)
    secondary_obj = kwargs.pop('secondary_obj', None)
    user = sender

    if not user.is_authenticated():
        new_page_view = PageView.objects.create(path=page_path,
                                                created=datetime.now())
    else:
        new_page_view = PageView.objects.create(path=page_path, user=user,
                                                created=datetime.now())

    if primary_obj:
        new_page_view.primary_object_id = primary_obj.id
        new_page_view.primary_content_type = ContentType.objects.get_for_model(
            primary_obj)

    if secondary_obj:
        new_page_view.secondary_object_id = secondary_obj.id
        new_page_view.secondary_content_type = ContentType.objects.get_for_model(
            secondary_obj)

    new_page_view.save()

page_view.connect(page_view_received)


@receiver(post_save, sender=PageView)
def clear_cache(sender, instance, created, **kwargs):
    cache._cache.flush_all()
