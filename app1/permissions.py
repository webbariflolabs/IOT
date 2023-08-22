from rest_framework import permissions

class CanCreateUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class CanEditUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user

class CanDeleteUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

