from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from notifications.models import Notification


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    recipient_url = serializers.SerializerMethodField()
    sender = serializers.CharField(source='sender_object', read_only=True)
    sender_url = serializers.SerializerMethodField()
    sender_profile_picture = serializers.ReadOnlyField(
        source="sender_object.default_profile_picture")
    view_target_photo_url = serializers.SerializerMethodField()
    target_photo = serializers.ReadOnlyField(
        source="target_object.get_photo_url")
    target_url = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'sender', 'sender_url', 'sender_profile_picture',
                  'display_thread', 'view_target_photo_url', 'target_photo',
                  'target_url', 'recipient_url', 'read',
                  'created', 'modified',)

    def get_recipient_url(self, obj):
        request = self.context['request']
        kwargs = {'username': obj.recipient.username}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)

    def get_sender_url(self, obj):
        request = self.context['request']
        kwargs = {'username': obj.sender_object.username}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)

    def get_view_target_photo_url(self, obj):
        request = self.context['request']
        if obj.target_object:
            kwargs = {
                'cat_slug': obj.target_object.category.slug,
                'photo_slug': obj.target_object.slug
            }
            return api_reverse('photo_detail_api', kwargs=kwargs,
                               request=request)
        return None

    def get_target_url(self, obj):
        request = self.context['request']
        if obj.action_object:
            if obj.verb == "liked":
                view_name = "photo_detail_api"
                kwargs = {
                    'cat_slug': obj.target_object.category.slug,
                    'photo_slug': obj.target_object.slug
                }
                return api_reverse(view_name, kwargs=kwargs, request=request)
            elif obj.verb == "commented":
                view_name = "comment_detail_api"
                kwargs = {'id': obj.action_object.id}
                return api_reverse(view_name, kwargs=kwargs, request=request)
        return None
