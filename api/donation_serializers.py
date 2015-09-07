from rest_framework import permissions, serializers, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.reverse import reverse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from donations.models import Donation


class MyUserUrlField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, view_name, request, format):
        kwargs = {
            'username': obj.user.username
        }
        return reverse(view_name, kwargs=kwargs,
                       request=request, format=format)


class DonationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_url = MyUserUrlField("user_profile_detail_api")

    class Meta:
        model = Donation
        fields = [
            'id',
            'user',
            'user_url',
            'amount',
            'message',
            'is_anonymous',
            'created',
            'modified',
        ]


class DonationViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication,
                              JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
