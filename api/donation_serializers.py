from rest_framework import serializers
from rest_framework.reverse import reverse

from donations.models import Donation


class MyUserUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {'username': obj.user.username}
        return reverse(view_name, kwargs=kwargs, request=request,
                       format=format)


class DonationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_url = MyUserUrlField("user_account_detail_api")

    class Meta:
        model = Donation
        fields = ['id', 'user', 'user_url', 'amount', 'message',
                  'is_anonymous', 'created', 'modified']
