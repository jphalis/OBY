from __future__ import absolute_import

from rest_framework.viewsets import ModelViewSet

from push_notifications.models import APNSDevice, GCMDevice

from .mixins import AuthorizedMixin, DeviceViewSetMixin
from .serializers import APNSDeviceSerializer, GCMDeviceSerializer


class APNSDeviceViewSet(DeviceViewSetMixin, ModelViewSet):
    queryset = APNSDevice.objects.all()
    serializer_class = APNSDeviceSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            name=self.request.data.get('name'),
            registration_id=self.request.data.get('registration_id'),
            device_id=self.request.data.get('device_id'))


class APNSDeviceAuthorizedViewSet(AuthorizedMixin, APNSDeviceViewSet):
    pass


class GCMDeviceViewSet(DeviceViewSetMixin, ModelViewSet):
    queryset = GCMDevice.objects.all()
    serializer_class = GCMDeviceSerializer


class GCMDeviceAuthorizedViewSet(AuthorizedMixin, GCMDeviceViewSet):
    pass
