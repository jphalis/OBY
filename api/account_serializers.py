from rest_framework import permissions, serializers, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.reverse import reverse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from accounts.models import Follower, MyUser
from photos.models import Photo

from .photo_serializers import PhotoSerializer


class FollowerCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Follower
        fields = ('user', 'followers')


class FollowerUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):

        kwargs = {
            'username': obj.user.username
        }
        return reverse(view_name, kwargs=kwargs,
                       request=request, format=format)


class FollowerSerializer(serializers.HyperlinkedModelSerializer):
    # username = serializers.CharField(source='user.username', read_only=True)
    # user_url = FollowerUrlField("user_profile_detail_api")
    followers = FollowerUrlField("user_profile_detail_api", many=True)
    following = FollowerUrlField("user_profile_detail_api", many=True)

    class Meta:
        model = Follower
        fields = [
            # 'username',
            # 'user_url',
            'followers',
            'following',
        ]


class FollowerViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyUserUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'username': obj.username
        }
        return reverse(view_name, kwargs=kwargs,
                       request=request, format=format)


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    account_url = MyUserUrlField("user_profile_detail_api")
    follower = FollowerSerializer(read_only=True)
    photo_set = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = [
            'id',
            'account_url',
            'username',
            'email',
            'full_name',
            'bio',
            'website',
            'edu_email',
            'gender',
            'photo_set',
            'profile_picture',
            'follower',
            'is_active',
            'is_admin',
            'is_verified',
            'date_joined',
            'modified'
        ]

    def get_photo_set(self, request):
        queryset = Photo.objects.own(request.pk)
        serializer = PhotoSerializer(queryset, context=self.context,
                                     many=True, read_only=True)
        return serializer.data


class MyUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
