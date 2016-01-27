from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import Truncator

from core.models import TimeStampedModel
from hashtags.models import HashtagMixin
from photos.models import Photo

# Create your models here.


class CommentManager(models.Manager):
    def active(self):
        return super(CommentManager, self).select_related(
            'user', 'photo').filter(is_active=True, parent=None)

    def create_comment(self, user=None, text=None, path=None,
                       photo=None, parent=None):
        if not path:
            raise ValueError("Must include a path when adding a comment")
        if not user:
            raise ValueError("Must include a user when adding a comment")

        comment = self.model(
            user=user,
            path=path,
            text=text
        )
        if photo is not None:
            comment.photo = photo
            comment.save()
        if parent is not None:
            comment.parent = parent
            comment.save()
        return comment


class Comment(HashtagMixin, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", null=True, blank=True)
    path = models.CharField(max_length=350)
    photo = models.ForeignKey(Photo)
    text = models.TextField(max_length=240)
    hashtag_enabled_text = models.TextField(
        blank=True,
        help_text='Contains the description with hashtags replaced with links')
    hashtag_text_field = 'text'

    objects = CommentManager()

    class Meta:
        app_label = 'comments'
        ordering = ['-created']

    def __unicode__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('comments:comment_thread', kwargs={"id": self.id})

    def get_affected_users(self):
        """
        it needs to be a parent and have children,
        the children, in effect, are the affected users.
        """
        comment_children = self.get_children()
        if comment_children is not None:
            users = []
            for comment in comment_children:
                if comment.user not in users:
                    users.append(comment.user)
                    return users
        return None

    def get_children(self):
        if self.is_child:
            return None
        return Comment.objects.filter(parent=self)

    def get_children_count(self):
        if self.is_child:
            return None
        return Comment.objects.filter(parent=self).count()

    @property
    def get_comment(self):
        return self.text

    @property
    def get_origin(self):
        return self.path

    @property
    def get_preview(self):
        return Truncator(self.text).chars(160)

    @property
    def is_child(self):
        return self.parent is not None
