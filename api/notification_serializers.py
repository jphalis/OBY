from rest_framework import serializers

from notifications.models import Notification
from .url_fields import (NotificationRecipientUrlField,
                         NotificationSenderUrlField, NotificationTargetUrl)


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    recipient = NotificationRecipientUrlField("user_account_detail_api")
    sender = serializers.CharField(source='sender_object', read_only=True)
    sender_url = NotificationSenderUrlField("user_account_detail_api")
    sender_profile_picture = serializers.ReadOnlyField(
        source="sender_object.default_profile_picture")
    target_photo = serializers.ReadOnlyField(
        source="target_object.get_photo_url")
    target_url = NotificationTargetUrl("")

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'sender_url', 'sender_profile_picture',
                  'display_thread', 'target_photo', 'target_url', 'recipient',
                  'read', 'created', 'modified']
