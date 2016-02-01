from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from accounts.models import Advertiser


class MyUserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # if request.user.is_authenticated == False:
        #   return False
        return obj.username == request.user.get_username()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user


class IsAdvertiser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if Advertiser.objects.get(user=request.user):
                return True
            else:
                raise PermissionDenied(
                    'You must be an advertiser to view this.')
        raise PermissionDenied('You must be signed in to view this.')
