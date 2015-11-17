from rest_framework import serializers

from accounts.models import Follower, MyUser
from photos.models import Photo
from .photo_serializers import PhotoSerializer
from .url_fields import FollowerUrlField, MyUserUrlField


class FollowerCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Follower
        fields = ['user', 'followers']


class FollowerSerializer(serializers.HyperlinkedModelSerializer):
    # username = serializers.CharField(source='user.username', read_only=True)
    followers = FollowerUrlField("user_account_detail_api", many=True)
    following = FollowerUrlField("user_account_detail_api", many=True)

    class Meta:
        model = Follower
        fields = ['followers', 'following']


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # update username validation requirements
        # make password >= 3 characters
        user = MyUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    account_url = MyUserUrlField("user_account_detail_api")
    follower = FollowerSerializer(read_only=True)
    photo_set = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['id', 'account_url', 'username', 'email', 'full_name', 'bio',
                  'website', 'edu_email', 'gender', 'photo_set',
                  'profile_picture', 'follower', 'is_active', 'is_admin',
                  'is_verified', 'date_joined', 'modified']

    def get_photo_set(self, request):
        queryset = Photo.objects.own(request.pk)
        serializer = PhotoSerializer(queryset, context=self.context, many=True,
                                     read_only=True)
        return serializer.data
