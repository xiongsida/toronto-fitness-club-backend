from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class isDebugingOrSecretForGet(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'GET':
            return True
        else:
            from django.conf import settings
            return getattr(settings, "DEBUG", None)


class IsTheUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj.user == request.user


class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


# class hasPlan(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.user != None and hasattr(request.user, 'subscription'):
#             return has_plan(request.user, request.user.subscription)
#         else:
#             return False
