# from __future__ import unicode_literals

# from django.conf import settings
# from django.core.urlresolvers import reverse
# from django.db import models

# # Create your models here.


# def upload_location(instance, filename):
#     return "{}/messages/photos/{}".format(instance.user.username, filename)


# class DirectMessage(models.Model):
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender')
#     recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                   related_name='receiver')
#     body = models.TextField(max_length=500, null=True)
#     image = models.ImageField(upload_to=upload_location, null=True, blank=True)
#     sent = models.DateTimeField(null=True, blank=True)
#     read_at = models.DateTimeField(null=True, blank=True)
#     opened = models.BooleanField(default=False)
#     # expiration_date = models.DurationField(null=True, blank=True)
#     parent = models.ForeignKey('self', related_name='parent_message',
#                                null=True, blank=True)
#     replied = models.BooleanField(default=False)

#     class Meta:
#         ordering = ['-sent']
#         app_label = 'directmessages'

#     def __unicode__(self):
#         return u"{}".format(self.sender)

#     def get_absolute_url(self):
#         return reverse('view_direct_message', kwargs={"id": self.id})

#     def get_reply_url(self):
#         return reverse('reply', kwargs={"id": self.id})
