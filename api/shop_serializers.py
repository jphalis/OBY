from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from shop.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'description', 'cost', 'max_downloads',
                  'promo_code', 'list_date_start',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='owner.user.username')
    owner_url = serializers.SerializerMethodField()
    buyers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        # add company logo
        fields = ('id', 'is_listed', 'is_featured', 'owner', 'owner_url',
                  'title', 'slug', 'description', 'cost', 'discount_cost',
                  'promo_code', 'get_buyer_usernames', 'is_useable',
                  'max_downloads', 'list_date_start', 'list_date_end',
                  'use_date_start', 'use_date_end',)

    def get_owner_url(self, obj):
        request = self.context['request']
        kwargs = {'username': obj.owner.user.username}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)
