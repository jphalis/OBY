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


class NotificationSenderProfilePicture(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'profile_picture': obj.sender_object.profile_picture}
        return reverse(view_name, kwargs=kwargs, request=request,
                       format=format)


class NotificationTargetUrl(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.target_object.slug:
            kwargs = {
                'cat_slug': obj.target_object.category.slug,
                'photo_slug': obj.target_object.slug
            }
            return reverse(view_name, kwargs=kwargs, request=request,
                           format=format)
        else:
            return None


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    recipient = NotificationRecipientUrlField("user_account_detail_api")
    sender = serializers.CharField(source='sender_object', read_only=True)
    sender_url = NotificationSenderUrlField("user_account_detail_api")
    sender_profile_picture = serializers.ReadOnlyField(
        source="sender_object.default_profile_picture")
    # action = serializers.CharField(source='action_object', read_only=True)
    # target_id = serializers.CharField(source='target_object_id',
                                      # read_only=True)
    # target_slug = serializers.CharField(
        # source='target_object', read_only=True)
    target_photo = serializers.ReadOnlyField(
        source="target_object.get_photo_url")
    target_url = NotificationTargetUrl("photo_detail_api")

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'sender_url', 'sender_profile_picture',
                  'display_thread', 'target_photo', 'target_url', 'recipient',
                  'read', 'created', 'modified']
