from datetime import datetime
# from urlparse import urlparse

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel
from core.utils import readable_number

# Create models here.


def upload_location(instance, filename):
    return "{}/profile_pictures/{}".format(instance.username, filename)


class MyUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        if not username:
            raise ValueError('Users must have a username')

        if not email:
            raise ValueError('Users must have an email address')

        now = datetime.now()
        user = self.model(
            username=username, email=self.normalize_email(email),
            date_joined=now, last_login=now
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  password):
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email',
                              max_length=80, unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    website = models.CharField(max_length=90, blank=True)
    edu_email = models.EmailField(verbose_name='.edu email', max_length=80,
                                  null=True, blank=True)
    GENDER_CHOICES = (
        ('Dude', _('Dude')),
        ('Betty', _('Betty')),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              blank=True)
    profile_picture = models.ImageField(upload_to=upload_location, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    times_flagged = models.PositiveIntegerField(default=0)
    stripe_customer_id = models.CharField(max_length=30, editable=False,
                                          blank=True)
    available_points = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    # points_at_last_check = models.IntegerField(default=0)
    # last_point_check = models.DateTimeField()
    blocking = models.ManyToManyField('self', related_name='blocked_by',
                                      symmetrical=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        app_label = 'accounts'

    def __unicode__(self):
        return u"{}".format(self.username)

    def get_profile_view(self):
        return reverse('profile_view', kwargs={"username": self.username})

    @cached_property
    def get_short_name(self):
        return "{}".format(self.full_name)

    @cached_property
    def get_full_name(self):
        return "{}".format(self.full_name)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    @property
    def default_profile_picture(self):
        if self.profile_picture:
            return "{}{}".format(settings.MEDIA_URL, self.profile_picture)
        return settings.STATIC_URL + 'img/default_profile_picture.jpg'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Follower(TimeStampedModel):
    user = models.OneToOneField(MyUser)
    followers = models.ManyToManyField('self', related_name='following',
                                       symmetrical=False)

    class Meta:
        ordering = ['-created']
        app_label = 'accounts'

    def __unicode__(self):
        return u'{}'.format(self.user.username)

    @cached_property
    def get_followers_usernames(self):
        return map(str, self.followers.values_list(
                   'user__username', flat=True))

    @cached_property
    def get_following_usernames(self):
        return map(str, self.following.values_list(
                   'user__username', flat=True))

    @cached_property
    def get_followers_info(self):
        return self.followers.select_related('user').values(
            'user__username', 'user__full_name', 'user__profile_picture')

    @cached_property
    def get_following_info(self):
        return self.following.select_related('user').values(
            'user__username', 'user__full_name', 'user__profile_picture')

    @cached_property
    def get_followers_url(self):
        return reverse('followers_thread',
                       kwargs={'username': self.user.username})

    @cached_property
    def get_following_url(self):
        return reverse('following_thread',
                       kwargs={'username': self.user.username})

    def get_followers_count(self, short=True):
        count = self.get_followers_info.count()
        return readable_number(count, short=short)

    def get_following_count(self, short=True):
        count = self.get_following_info.count()
        return readable_number(count, short=short)

MyUser.profile = property(lambda u: Follower.objects.get_or_create(user=u)[0])


class Advertiser(TimeStampedModel):
    USER_STATUSES = (
        (0, _('Pending review')),
        (1, _('In review')),
        (2, _('Approved')),
        (3, _('Declined')),
        (4, _('Black listed'))
    )
    user_status = models.IntegerField(choices=USER_STATUSES,
                                      default=USER_STATUSES[0][0])
    user = models.OneToOneField(MyUser)
    company_name = models.CharField(max_length=120, blank=True)
    description = models.TextField(max_length=200, blank=True)
    company_website = models.CharField(max_length=90, blank=True)
    twitter = models.CharField(max_length=80, blank=True)
    instagram = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=False)
    creations_allowed = models.IntegerField(default=0)

    class Meta:
        app_label = 'accounts'

    def __unicode__(self):
        return u"{}".format(self.user.username)

    # Not working
    # @cached_property
    # def hyperlink_company_website(self):
    #     return "http://www.{}".format(urlparse(self.company_website).netloc)

    @cached_property
    def hyperlink_twitter(self):
        return "http://www.twitter.com/{}".format(self.twitter)

    @cached_property
    def hyperlink_instagram(self):
        return "http://www.instagram.com/{}".format(self.twitter)


# def new_user_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         new_profile, is_created = MyUser.objects.get_or_create(user=instance)

# post_save.connect(new_user_receiver, sender=MyUser)
