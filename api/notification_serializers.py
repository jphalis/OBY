from rest_framework import serializers
from rest_framework.reverse import reverse

from notifications.models import Notification


class NotificationRecipientUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.recipient.username}
        return reverse(view_name, kwargs=kwargs, request=request,
                       format=format)


class NotificationSenderUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.sender_object.username}
        return reverse(view_name, kwargs=kwargs, request=request,
                       format=format)


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    recipient = NotificationRecipientUrlField("user_account_detail_api")
    sender = serializers.CharField(source='sender_object', read_only=True)
    sender_url = NotificationSenderUrlField("user_account_detail_api")
    action = serializers.CharField(source='action_object', read_only=True)
    target_id = serializers.CharField(source='target_object_id',
                                      read_only=True)
    target_slug = serializers.CharField(source='target_object', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'sender', 'sender_url', 'verb', 'action', 'target_id',
                  'target_slug', 'recipient', 'read', 'created', 'modified')
