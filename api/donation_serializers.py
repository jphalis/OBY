from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from donations.models import Donation


class DonationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_url = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = ('id', 'user', 'user_url', 'amount', 'message',
                  'is_anonymous', 'created', 'modified',)

    def get_user_url(self, obj):
        request = self.context['request']
        kwargs = {'username': obj.user.username}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)
