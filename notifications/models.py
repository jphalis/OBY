from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

from core.models import TimeStampedModel

# Create your models here.


class NotificationQuerySet(models.query.QuerySet):
    def get_user(self, recipient):
        return self.filter(recipient=recipient)

    def mark_all_read(self, recipient):
        qs = self.get_user(recipient).unread()
        qs.update(read=True)

    def mark_all_unread(self, recipient):
        qs = self.get_user(recipient).read()
        qs.update(read=False)

    def mark_targetless(self, recipient):
        qs = self.get_user(recipient).unread()
        qs_no_target = qs.filter(target_object_id=None)
        if qs_no_target:
            qs_no_target.update(read=True)

    def read(self):
        return self.filter(read=True)

    def recent(self):
        return self.unread()[:5]

    def unread(self):
        return self.filter(read=False)


class NotificationManager(models.Manager):
    def all_for_user(self, user):
        self.get_queryset().mark_targetless(user)
        return self.get_queryset().get_user(user)

    def all_read(self, user):
        return self.get_queryset().get_user(user).read()

    def all_unread(self, user):
        return self.get_queryset().get_user(user).unread()

    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def get_recent_for_user(self, user, num):
        return self.get_queryset().get_user(user)[:num]


class Notification(TimeStampedModel):
    # JP
    sender_content_type = models.ForeignKey(ContentType,
                                            related_name='nofity_sender')
    sender_object_id = models.PositiveIntegerField()
    sender_object = GenericForeignKey("sender_content_type",
                                      "sender_object_id")
    # Commented
    verb = models.CharField(max_length=255)
    # "What's up?""
    action_content_type = models.ForeignKey(ContentType,
                                            related_name='notify_action',
                                            null=True, blank=True)
    action_object_id = models.PositiveIntegerField(null=True, blank=True)
    action_object = GenericForeignKey("action_content_type",
                                      "action_object_id")
    # On your photo
    target_content_type = models.ForeignKey(ContentType,
                                            related_name='notify_target',
                                            null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey("target_content_type",
                                      "target_object_id")
    # Annie
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='notifications')
    read = models.BooleanField(default=False)

    objects = NotificationManager()

    class Meta:
        ordering = ['-created']
        app_label = 'notifications'

    def __unicode__(self):
        try:
            target_url = self.target_object.get_absolute_url()
        except:
            target_url = None

        context = {
            "action": self.action_object,
            "sender": self.sender_object,
            "sender_url": self.sender_object.get_profile_view(),
            "target": self.target_object,
            "target_url": target_url,
            "verb": self.verb,
        }

        if self.target_object:
            if self.action_object:
                # New Like
                if self.verb == "liked":
                    return "<a href='%(sender_url)s'>%(sender)s</a> %(verb)s your picture" % context
                # New Comment
                elif self.verb == "commented":
                    return '<a href="%(sender_url)s">%(sender)s</a> %(verb)s: "%(action)s"' % context
                # Other
                else:
                    return "<a href='%(sender_url)s'>%(sender)s</a> %(verb)s %(action)s" % context
        else:
            # No target object
            return "<a href='%(sender_url)s'>%(sender)s</a> %(verb)s" % context
        return "%(sender)s %(verb)s" % context

    def display_thread(self):
        try:
            target_url = self.target_object.get_absolute_url()
        except:
            target_url = None

        context = {
            "action": self.action_object,
            "sender": self.sender_object,
            "sender_url": self.sender_object.get_profile_view(),
            "target": self.target_object,
            "target_url": target_url,
            "verb": self.verb,
        }

        if self.target_object:
            if self.action_object:
                # New Like
                if self.verb == "liked":
                    return "%(sender)s %(verb)s your picture" % context
                # New Comment
                elif self.verb == "commented":
                    return "%(sender)s %(verb)s: '%(action)s'" % context
                # Other
                else:
                    return "%(sender)s %(verb)s %(action)s" % context
        else:
            # No target object
            return "%(sender)s %(verb)s" % context
        return "%(sender)s %(verb)s" % context

    def get_photo_url(self):
        try:
            target_url = self.target_object.get_absolute_url()
        except:
            target_url = reverse("notifications_all")

        context = {
            "target": self.target_object,
            "target_url": target_url,
        }

        if self.target_object:
            return "%(target_url)s" % context
        else:
            pass
