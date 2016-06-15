from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from comments.models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'username', 'parent', 'photo', 'text',)


class CommentUpdateSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'children',)

    def get_children(self, instance):
        queryset = Comment.objects.filter(parent__pk=instance.pk)
        serializer = ChildCommentSerializer(queryset, many=True,
                                            context={"request": instance})
        return serializer.data


class ChildCommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text',)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    photo_url = serializers.SerializerMethodField()
    comment_url = serializers.HyperlinkedIdentityField(
        "comment_detail_api", lookup_field='id')
    user = serializers.HyperlinkedRelatedField(
        view_name='user_account_detail_api', read_only=True,
        lookup_field='username')
    text = serializers.CharField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'photo_url', 'comment_url', 'user', 'text',
                  'children',)

    def get_photo_url(self, obj):
        request = self.context['request']
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
            return api_reverse('photo_detail_api', kwargs=kwargs,
                               request=request)
        return None

    def get_children(self, instance):
        queryset = Comment.objects.filter(parent__pk=instance.pk)
        serializer = ChildCommentSerializer(queryset, many=True,
                                            context={"request": instance})
        return serializer.data
