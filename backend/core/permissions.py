from rest_framework import permissions


class DenyAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class CreateOrCurrentUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST" or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk
