from rest_framework import serializers

from photos.models import Category, Photo
from .comment_serializers import CommentSerializer
from .url_fields import CategoryUrlField, PhotoCreatorUrlField, PhotoUrlField


class PhotoSerializer(serializers.ModelSerializer):
    category_url = CategoryUrlField("category_detail_api")
    photo_url = PhotoUrlField("photo_detail_api")
    creator = serializers.CharField(source='creator.username', read_only=True)
    creator_url = PhotoCreatorUrlField("user_account_detail_api")
    likers = serializers.HyperlinkedRelatedField(
        many=True, view_name='user_account_detail_api', read_only=True,
        lookup_field='username')
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'category_url', 'photo_url', 'slug', 'creator',
                  'creator_url', 'photo', 'description', 'like_count',
                  'likers', 'comment_count', 'comment_set', 'created',
                  'modified']


class PhotoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['photo', 'category', 'description']


class CategorySerializer(serializers.ModelSerializer):
    category_url = serializers.HyperlinkedIdentityField('category_detail_api',
                                                        lookup_field='slug')
    photo_set = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'border_color', 'category_url', 'slug', 'title',
                  'photo_set']

    def get_photo_set(self, request):
        queryset = Photo.objects.category_detail(request.pk)
        serializer = PhotoSerializer(queryset, context=self.context, many=True,
                                     read_only=True)
        return serializer.data
