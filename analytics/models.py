from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from photos.models import Category, Photo


class PageViewQuerySet(models.query.QuerySet):
    def categories(self):
        content_type = ContentType.objects.get_for_model(Category)
        return self.filter(primary_content_type=content_type)

    def photos(self):
        content_type = ContentType.objects.get_for_model(Photo)
        return self.filter(primary_content_type=content_type)

    def users(self):
        content_type = ContentType.objects.get_for_model(
            settings.AUTH_USER_MODEL)
        return self.filter(primary_content_type=content_type)


class PageViewManager(models.Manager):
    def get_queryset(self):
        return PageViewQuerySet(self.model, using=self._db)

    def get_categories(self):
        return self.get_queryset().categories()

    def get_photos(self):
        return self.get_queryset().photos()

    def get_users(self):
        return self.get_queryset().users()


class PageView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    path = models.CharField(max_length=350)

    primary_content_type = models.ForeignKey(ContentType,
                                             related_name='primary_obj',
                                             null=True, blank=True)
    primary_object_id = models.PositiveIntegerField(null=True, blank=True)
    primary_object = GenericForeignKey("primary_content_type",
                                       "primary_object_id")

    secondary_content_type = models.ForeignKey(ContentType,
                                               related_name='secondary_obj',
                                               null=True, blank=True)
    secondary_object_id = models.PositiveIntegerField(null=True, blank=True)
    secondary_object = GenericForeignKey("secondary_content_type",
                                         "secondary_object_id")

    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PageViewManager()

    def __unicode__(self):
        return u"{}".format(self.path)

    class Meta:
        ordering = ['-timestamp']
