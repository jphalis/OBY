from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count, Q

from datetime import datetime, timedelta

from hashtags.models import HashtagMixin

# Create your models here.


def upload_location(instance, filename):
    return "{}/photos/{}".format(instance.creator.username, filename)


class PhotoManager(models.Manager):
    def category_detail(self, obj):
        date_from = datetime.now() - timedelta(days=21)
        return super(PhotoManager, self).get_queryset().annotate(
            the_count=(Count('likers'))).filter(
                is_active=True, timestamp__gte=date_from,
                category=obj).order_by('-the_count')

    def most_commented(self):
        return super(PhotoManager, self).get_queryset().annotate(
            the_count=(Count('comment'))).filter(
                is_active=True).order_by('-the_count')

    def most_liked(self):
        return super(PhotoManager, self).get_queryset().annotate(
            the_count=(Count('likers'))).filter(
                is_active=True).order_by('-the_count')

    def most_liked_offset(self):
        date_from = datetime.now() - timedelta(days=21)
        return super(PhotoManager, self).get_queryset().annotate(
            the_count=(Count('likers'))).filter(
                is_active=True, timestamp__gte=date_from).order_by(
                    '-the_count')

    def own(self, user):
        return super(PhotoManager, self).get_queryset().select_related(
            'category', 'creator').filter(creator=user)

    def following(self, user):
        return super(PhotoManager, self).get_queryset().select_related(
            'creator').filter(
                creator__follower__in=user.follower.following.all())


class Photo(HashtagMixin, models.Model):
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey("Category")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField(max_length=250, blank=True)
    hashtag_enabled_description = models.TextField(blank=True,
        help_text='Contains the description with hashtags replaced with links')
    featured = models.BooleanField(default=False)
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='likers', blank=True)
    photo = models.ImageField(upload_to=upload_location)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)

    hashtag_text_field = 'description'

    objects = PhotoManager()

    class Meta:
        unique_together = ('slug', 'category',)
        ordering = ['-timestamp']
        app_label = 'photos'

    def __unicode__(self):
        return u"{}".format(self.slug)

    def get_comments_all(self):
        return reverse('comments_all', kwargs={"cat_slug": self.category.slug,
                                               "photo_slug": self.slug})

    def get_photo_url(self):
        return "{}{}".format(settings.MEDIA_URL, self.photo)

    def get_delete_url(self):
        return reverse('delete_photo', kwargs={"pk": self.pk})

    def get_likers_usernames(self):
        return map(str, self.likers.all().values_list('username', flat=True))

    def like_count(self):
        return self.likers.count()


class CategoryManager(models.Manager):
    def get_all(self):
        return self.get_queryset().filter(is_active=True)

    def get_featured(self):
        return self.get_queryset().filter(is_active=True, featured=True)

    def most_posts(self):
        return super(CategoryManager, self).get_queryset().annotate(
            the_count=(Count('photo'))).filter(
                is_active=True).order_by('-the_count')


class Category(models.Model):
    is_active = models.BooleanField(default=True)
    border_color = models.CharField(default='#', max_length=7)
    featured = models.BooleanField(default=False)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    class Meta:
        app_label = 'photos'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"cat_slug": self.slug})
