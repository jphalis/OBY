from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from shop.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'image', 'description', 'cost', 'discount_cost',
                  'max_downloads', 'promo_code', 'list_date_start',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='owner.username')
    owner_url = serializers.SerializerMethodField()
    buyers = serializers.StringRelatedField(many=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'is_listed', 'is_featured', 'owner', 'owner_url',
                  'title', 'slug', 'image', 'description', 'cost',
                  'discount_cost', 'promo_code', 'buyers', 'is_useable',
                  'max_downloads', 'list_date_start', 'list_date_end',
                  'use_date_start', 'use_date_end',)

    def get_owner_url(self, obj):
        request = self.context['request']
        kwargs = {'username': obj.owner.username}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)
