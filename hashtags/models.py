from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class Hashtag(models.Model):
    tag = models.SlugField(max_length=250, unique=True)

    class Meta:
        app_label = 'hashtags'

    def __unicode__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('hashtag_detail', kwargs={'hashtag': str(self.tag)})


class HashtagMixin(models.Model):
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    hashtag_text_field = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(HashtagMixin, self).__init__(*args, **kwargs)

        # some defensive coding to ensure the field defined is a
        # CharField or TextField, especially when open sourcing
        if not self.hashtag_text_field:
            raise NotImplemented(u'You must define a source for the hashtags '
                u'to derive from, which needs to be a CharField or TextField.')

        self.hashtag_field = self._meta.get_field(self.hashtag_text_field)

        if not isinstance(self.hashtag_field,
                          (models.CharField, models.TextField,)):
            raise Exception(u'"hashtag_text_field" must be of type: '
                u'models.CharField or TextField.')

    def _get_hashtags(self):
        # split the string if the word starts with '#'
        return [str(word[1:]) for word in self.hashtag_field.value_to_string(
            self).split() if word.startswith('#')]

    def _delete_hashtags(self):
        # remove any previously set tags for the instance
        self.hashtags.clear()
        self.hashtags.all().delete()

    def _set_hashtags(self):
        self._delete_hashtags()

        # add any hashtags derived from the hashtag_text_field
        # makes all tags lowercase
        hashtags = []
        for tag in self._get_hashtags():
            hashtag, created = Hashtag.objects.get_or_create(
                tag=tag.lower(), defaults={'tag': tag.lower()})
            hashtags.append(hashtag)

        self.hashtags.add(*hashtags)

    def save(self, *args, **kwargs):
        super(HashtagMixin, self).save(*args, **kwargs)
        self._set_hashtags()
