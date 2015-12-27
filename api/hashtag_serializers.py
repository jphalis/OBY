from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from hashtags.models import Hashtag
from photos.models import Photo
from .comment_serializers import CommentSerializer


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'tag',)


class HashtagPhotoSerializer(serializers.ModelSerializer):
    category_url = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    creator = serializers.CharField(source='creator.username', read_only=True)
    creator_url = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True, read_only=True)
    like_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('id', 'category_url', 'photo_url', 'slug', 'creator',
                  'creator_url', 'photo', 'description', 'like_url',
                  'like_count', 'get_likers_info', 'comment_count',
                  'comment_set', 'created', 'modified')

    def get_category_url(self, obj):
        request = self.context['request']
        kwargs = {'slug': obj.category.slug}
        return api_reverse('category_detail_api', kwargs=kwargs,
                           request=request)

    def get_photo_url(self, obj):
        request = self.context['request']
        kwargs = kwargs = {
            'cat_slug': obj.category.slug,
            'photo_slug': obj.slug
        }
        return api_reverse('photo_detail_api', kwargs=kwargs, request=request)

    def get_creator_url(self, obj):
        request = self.context['request']
        kwargs = {'username': obj.creator.username}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)

    def get_like_url(self, obj):
        request = self.context['request']
        kwargs = {'photo_pk': obj.pk}
        return api_reverse('like_create_api', kwargs=kwargs, request=request)
