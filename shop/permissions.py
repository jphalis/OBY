# from rest_framework import permissions
# from rest_framework.exceptions import PermissionDenied


# class IsOwnerOrReadOnly(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # if request.user.is_authenticated == False:
#         #   return False

#         return obj.creator == request.user  # true/false


# class IsAdvertiser(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.user.is_authenticated():
#             if request.user.is_advertiser:
#                 return True
#             else:
#                 raise PermissionDenied(
#                     'You must be an advertiser to view this.')
#         raise PermissionDenied('You must be signed in to view this.')
