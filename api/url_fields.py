from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse


# A C C O U N T S  /  S E A R C H
class FollowerUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):

        kwargs = {'username': obj.user.username}
        return api_reverse(view_name, kwargs=kwargs, request=request,
                           format=format)


class MyUserUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.username}
        return api_reverse(view_name, kwargs=kwargs, request=request,
                           format=format)


# C O M M E N T S
class CommentPhotoUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        photo = None

        if obj.is_child:
            try:
                photo = obj.parent.photo
            except:
                photo = None
        else:
            try:
                photo = obj.photo
            except:
                photo = None

        if photo:
            kwargs = {
                'cat_slug': obj.photo.category.slug,
                'photo_slug': obj.photo.slug
            }
            return api_reverse(view_name, kwargs=kwargs, request=request,
                               format=format)
        return None


# D O N A T I O N S
class DonationUserUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.user.username}
        return api_reverse(view_name, kwargs=kwargs, request=request,
                           format=format)


# N O T I F I C A T I O N S
class NotificationRecipientUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.recipient.username}
        return api_reverse(view_name, kwargs=kwargs, request=request,
                           format=format)


class NotificationSenderUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.sender_object.username}
        return api_reverse(view_name, kwargs=kwargs, request=request,
                           format=format)


class NotificationTargetUrl(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        if obj.action_object:
            if obj.verb == "liked":
                view_name = "photo_detail_api"
                kwargs = {
                    'cat_slug': obj.target_object.category.slug,
                    'photo_slug': obj.target_object.slug
                }
                return api_reverse(view_name, kwargs=kwargs, request=request,
                                   format=format)
            if obj.verb == "commented":
                view_name = "comment_detail_api"
                kwargs = {
                    'id': obj.action_object.id
                }
                return api_reverse(view_name, kwargs=kwargs, request=request,
                                   format=format)
        return None


# P H O T O S
class PhotoCreatorUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.creator.username}
        return api_reverse(view_name, kwargs=kwargs, request=request,
                           format=format)


class CategoryUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'slug': obj.category.slug}
        return api_reverse(view_name, kwargs=kwargs, request=request,
                           format=format)


class PhotoUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'cat_slug': obj.category.slug,
            'photo_slug': obj.slug
        }
        return api_reverse(view_name, kwargs=kwargs, request=request,
                           format=format)
