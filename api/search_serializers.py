from rest_framework import serializers

from accounts.models import MyUser
from .url_fields import MyUserUrlField


class SearchMyUserSerializer(serializers.HyperlinkedModelSerializer):
    account_url = MyUserUrlField("user_account_detail_api")

    class Meta:
        model = MyUser
        fields = ['id', 'account_url', 'username', 'full_name',
                  'profile_picture']
