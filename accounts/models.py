from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel

# Create models here.


def upload_location(instance, filename):
    return "{}/profile_pictures/{}".format(instance.username, filename)


class MyUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        if not username:
            raise ValueError('Must include username')

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
    # USER_TYPES = (
    #     (0, _('Admin')),
    #     (1, _('Staff')),
    #     (2, _('Default')),
    #     (3, _('Verified')),
    #     (4, _('Advertiser')),
    # )
    # user_type = models.IntegerField(max_length=1, null=True,
    #                                 choices=USER_TYPES)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email',
                              max_length=80, unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    website = models.CharField(max_length=90, blank=True)
    edu_email = models.EmailField(verbose_name='.edu email', max_length=80,
                                  unique=True, null=True, blank=True)
    GENDER_CHOICES = (
        ('DUDE', _('Dude')),
        ('BETTY', _('Betty')),
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              blank=True)
    profile_picture = models.ImageField(upload_to=upload_location, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    stripe_customer_id = models.CharField(max_length=30, editable=False,
                                          blank=True)
    # Use when points are introduced
    # available_points = models.IntegerField(default=0)
    # total_points = models.IntegerField(default=0)
    # points_at_last_check = models.IntegerField(default=0)
    # last_point_check = models.DateTimeField()
    # creations_allowed = models.IntegerField(default=0)

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
        return map(str, self.followers.all().values_list(
                   'user__username', flat=True))

    @cached_property
    def get_following_usernames(self):
        return map(str, self.following.all().values_list(
                   'user__username', flat=True))

    @cached_property
    def get_followers_info(self):
        return self.followers.select_related('user').all().values(
            'user__username', 'user__full_name', 'user__profile_picture')

    @cached_property
    def get_following_info(self):
        return self.following.select_related('user').all().values(
            'user__username', 'user__full_name', 'user__profile_picture')

    @cached_property
    def get_followers_url(self):
        return reverse('followers_thread',
                       kwargs={'username': self.user.username})

    @cached_property
    def get_following_url(self):
        return reverse('following_thread',
                       kwargs={'username': self.user.username})

MyUser.profile = property(lambda u: Follower.objects.get_or_create(user=u)[0])


# def new_user_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         new_profile, is_created = UserProfile.objects.get_or_create(user=instance)

# post_save.connect(new_user_receiver, sender=MyUser)
