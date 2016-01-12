import StringIO

from datetime import datetime, timedelta
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from django.utils.functional import cached_property

from core.models import TimeStampedModel
from core.utils import readable_number
from hashtags.models import HashtagMixin

# Create your models here.


def upload_location(instance, filename):
    return "{}/photos/{}".format(instance.creator.username, filename)


class PhotoManager(models.Manager):
    def active(self):
        return super(PhotoManager, self).get_queryset() \
            .filter(is_active=True) \
            .select_related('category', 'creator') \
            .prefetch_related('likers')

    def category_detail(self, obj):
        date_from = datetime.now() - timedelta(days=150)
        return super(PhotoManager, self).get_queryset() \
            .filter(is_active=True, created__gte=date_from, category=obj) \
            .select_related('category', 'creator') \
            .prefetch_related('likers') \
            .annotate(the_count=(Count('likers'))) \
            .order_by('-the_count')

    def following(self, user):
        return super(PhotoManager, self).get_queryset() \
            .filter(creator__follower__in=user.follower.following.all()) \
            .select_related('category', 'creator') \
            .prefetch_related('likers')

    def most_commented(self):
        return super(PhotoManager, self).get_queryset() \
            .filter(is_active=True) \
            .select_related('category', 'creator') \
            .prefetch_related('likers') \
            .annotate(the_count=(Count('comment'))) \
            .order_by('-the_count')

    def most_liked(self):
        return super(PhotoManager, self).get_queryset() \
            .filter(is_active=True) \
            .select_related('category', 'creator') \
            .prefetch_related('likers') \
            .annotate(the_count=(Count('likers'))) \
            .order_by('-the_count')

    def most_liked_offset(self):
        date_from = datetime.now() - timedelta(days=150)
        return super(PhotoManager, self).get_queryset() \
            .filter(is_active=True, created__gte=date_from) \
            .select_related('category', 'creator') \
            .prefetch_related('likers') \
            .annotate(the_count=(Count('likers'))) \
            .order_by('-the_count')

    def own(self, user):
        return super(PhotoManager, self).get_queryset() \
            .filter(creator=user) \
            .select_related('category', 'creator') \
            .prefetch_related('likers')


class Photo(HashtagMixin, TimeStampedModel):
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey("Category")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField(max_length=250, blank=True)
    hashtag_enabled_description = models.TextField(
        blank=True,
        help_text='Contains the description with hashtags replaced with links')
    featured = models.BooleanField(default=False)
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='likers', blank=True)
    photo = models.ImageField(upload_to=upload_location)
    slug = models.SlugField()

    hashtag_text_field = 'description'

    objects = PhotoManager()

    class Meta:
        unique_together = ('slug', 'category',)
        ordering = ['-created']
        app_label = 'photos'

    def __unicode__(self):
        return u"{}".format(self.slug)

    def save(self, *args, **kwargs):
        if self.photo:
            img = Image.open(StringIO.StringIO(self.photo.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # img.thumbnail(
            #     (self.photo.width/1.5, self.photo.height/1.5), Image.ANTIALIAS)
            output = StringIO.StringIO()
            img.save(output, format='JPEG', quality=70)
            output.seek(0)
            self.photo = InMemoryUploadedFile(
                output, 'ImageField',
                '{}.jpg'.format(self.photo.name.split('.')[0]),
                'image/jpeg', output.len, None)
        super(Photo, self).save(*args, **kwargs)

    def get_comments_all(self):
        return reverse('comments:comments_all',
                       kwargs={"cat_slug": self.category.slug,
                               "photo_slug": self.slug})

    @cached_property
    def get_photo_url(self):
        return "{}{}".format(settings.MEDIA_URL, self.photo)

    @cached_property
    def get_delete_url(self):
        return reverse('photos:delete_photo', kwargs={"pk": self.pk})

    @cached_property
    def get_likers_usernames(self):
        return map(str, self.likers.values_list('username', flat=True))

    @cached_property
    def get_likers_info(self):
        return self.likers.values(
            'username', 'full_name', 'profile_picture')

    def like_count(self, short=True):
        count = self.likers.count()
        return readable_number(count, short=short)

    def comment_count(self, short=True):
        count = self.comment_set.count()
        return readable_number(count, short=short)


class CategoryManager(models.Manager):
    def get_all(self):
        return self.get_queryset().filter(is_active=True)

    def get_featured(self):
        return self.get_queryset().filter(is_active=True, featured=True)

    def most_posts(self):
        return super(CategoryManager, self).get_queryset() \
            .filter(is_active=True) \
            .annotate(the_count=(Count('photo'))) \
            .order_by('-the_count')


class Category(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    border_color = models.CharField(default='#', max_length=7)
    featured = models.BooleanField(default=False)
    title = models.CharField(max_length=120)
    slug = models.SlugField()

    objects = CategoryManager()

    class Meta:
        app_label = 'photos'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("photos:category_detail",
                       kwargs={"cat_slug": self.slug})
