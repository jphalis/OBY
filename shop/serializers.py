from rest_framework import permissions, serializers, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.reverse import reverse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Product


class MyUserUrlField(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'username': obj.owner.username
        }
        return reverse(view_name, kwargs=kwargs,
                       request=request, format=format)


class ProductCreateSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Product
        fields = [
            'owner',
            'title',
            'slug',
            'image',
            'description',
            'cost',
            'discount_cost',
            'max_downloads',
            'promo_code',
            'list_date_start',
        ]


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='owner.username')
    owner_url = MyUserUrlField("user_profile_detail_api")
    buyers = serializers.StringRelatedField(many=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'listed',
            'featured',
            'owner',
            'owner_url',
            'title',
            'slug',
            'image',
            'description',
            'cost',
            'discount_cost',
            'promo_code',
            'buyers',
            'useable',
            'max_downloads',
            'list_date_start',
            'list_date_end',
            'use_date_start',
            'use_date_end',
        ]


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
