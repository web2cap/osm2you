from rest_framework import permissions


class AuthorAdminOrReadOnly(permissions.BasePermission):
    """All methods for Admin or Author.
    GET for All."""

    def has_permission(self, request, view):
        return request.method == "GET" or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method == "GET") or (
            obj.author == request.user or request.user.is_superuser
        )
