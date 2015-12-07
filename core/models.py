from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Permalinkable(models.Model):
    slug = models.SlugField()

    class Meta:
        abstract = True

    def get_url_kwargs(self, **kwargs):
        kwargs.update(getattr(self, 'url_kwargs', {}))
        return kwargs

    @models.permalink
    def get_absolute_url(self):
        url_kwargs = self.get_url_kwargs(slug=self.slug)
        return (self.url_name, (), url_kwargs)

    def pre_save(self, instance, add):
        if not instance.slug:
            instance.slug = slugify(self.slug_source)

    # Use this as a property in the individual model
    # @property
    # def slug_source(self):
    #     return self.title


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Userable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True
