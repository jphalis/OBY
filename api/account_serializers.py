from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from accounts.models import Follower, MyUser
# from oby.settings.approved_universities import APPROVED_UNIVERSITIES
from photos.models import Photo
from .photo_serializers import PhotoSerializer


class FollowerCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Follower
        fields = ('user', 'followers',)


class FollowerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Follower
        fields = ('get_followers_count', 'get_following_count',
                  'get_followers_info', 'get_following_info',)


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # update username validation requirements
        # update email validation requirements
        # make password >= 3 characters
        user = MyUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    account_url = serializers.SerializerMethodField()
    follower = FollowerSerializer(read_only=True)
    photo_set = serializers.SerializerMethodField()
    username = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    follow_url = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('id', 'account_url', 'username', 'email', 'full_name', 'bio',
                  'website', 'edu_email', 'gender', 'photo_set',
                  'profile_picture', 'follow_url', 'follower', 'is_active',
                  'is_admin', 'is_verified', 'date_joined', 'modified',)

    def get_account_url(self, obj):
        request = self.context['request']
        kwargs = {'username': obj.username}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)

    def get_follow_url(self, obj):
        request = self.context['request']
        kwargs = {'user_pk': obj.pk}
        return api_reverse('follow_create_api', kwargs=kwargs, request=request)

    def get_photo_set(self, request):
        queryset = Photo.objects.own(request.pk)
        serializer = PhotoSerializer(queryset, context=self.context, many=True,
                                     read_only=True)
        return serializer.data

    def validate_edu_email(self, value):
        if value:
            value = value.lower()
            username, domain = value.split('@')
            if not domain.endswith('.edu'):
                raise serializers.ValidationError(
                    "Please use a valid university email.")
            # if domain not in APPROVED_UNIVERSITIES:
            #     raise serializers.ValidationError(
            #         "Sorry, this university isn't registered with us yet. "
            #         "Email us to get it signed up! universities@obystudio.com")
            return value
        else:
            pass
