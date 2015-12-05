from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from accounts.models import MyUser


class SearchMyUserSerializer(serializers.HyperlinkedModelSerializer):
    account_url = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('id', 'account_url', 'username', 'full_name',
                  'profile_picture',)

    def get_account_url(self, obj):
        request = self.context['request']
        kwargs = {'username': obj.username}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)
