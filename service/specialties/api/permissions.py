from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """Permission to only allow admins to redact something"""
    def has_permission(self, request, view):
        """Check whether the user is admin"""
        admin_permission = bool(request.user and request.user.is_staff)
        if request.method in permissions.SAFE_METHODS:
            return True
        return admin_permission


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission to only allow owners to redact their own records"""
    def has_object_permission(self, request, view, obj):
        """Check whether the user is owner"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticated):
    """Permission to only allow authenticated users to do something"""
    def has_permission(self, request, view):
        """Check whether the user is authenticated"""
        user_permission = bool(request.user and request.user.is_authenticated)
        if request.method in permissions.SAFE_METHODS:
            return True
        return user_permission
