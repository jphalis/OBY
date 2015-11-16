from rest_framework import serializers

from donations.models import Donation
from .url_fields import DonationUserUrlField


class DonationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_url = DonationUserUrlField("user_account_detail_api")

    class Meta:
        model = Donation
        fields = ['id', 'user', 'user_url', 'amount', 'message',
                  'is_anonymous', 'created', 'modified']
