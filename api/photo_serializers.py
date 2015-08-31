from rest_framework import permissions, serializers, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.reverse import reverse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from photos.models import Category, Photo

from .comment_serializers import CommentSerializer


class MyUserUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'username': obj.creator.username
        }
        return reverse(view_name, kwargs=kwargs,
                       request=request, format=format)


class CategoryUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'slug': obj.category.slug
        }
        return reverse(view_name, kwargs=kwargs,
                       request=request, format=format)


class PhotoUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'cat_slug': obj.category.slug,
            'photo_slug': obj.slug
        }
        return reverse(view_name, kwargs=kwargs,
                       request=request, format=format)


class PhotoSerializer(serializers.ModelSerializer):
    category_url = CategoryUrlField("category_detail_api")
    photo_url = PhotoUrlField("photo_detail_api")
    creator = serializers.CharField(source='creator.username', read_only=True)
    creator_url = MyUserUrlField("user_profile_detail_api")
    likers = serializers.HyperlinkedRelatedField(
        many=True, view_name='user_profile_detail_api', read_only=True,
        lookup_field='username')
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = [
            'id',
            'category_url',
            'photo_url',
            'slug',
            'creator',
            'creator_url',
            'photo',
            'description',
            'like_count',
            'likers',
            'comment_set',
            'created',
            'modified',
        ]


class PhotoViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            'creator',
            'photo',
            'category',
            'description',
        ]


class CategorySerializer(serializers.ModelSerializer):
    category_url = serializers.HyperlinkedIdentityField('category_detail_api',
                                                        lookup_field='slug')
    photo_set = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'border_color',
            'category_url',
            'slug',
            'title',
            'photo_set',
        ]

    def get_photo_set(self, request):
        queryset = Photo.objects.category_detail(request.pk)
        serializer = PhotoSerializer(queryset, context=self.context,
                                     many=True, read_only=True)
        return serializer.data


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
