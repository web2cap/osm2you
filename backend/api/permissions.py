from rest_framework import permissions


class AuthorAdminOrReadOnly(permissions.BasePermission):
    """POST, PATCH, DELETE methods for Admin or Author. GET for All."""

    write_allow_methods = ("POST", "PATCH", "DELETE")

    def has_permission(self, request, view):
        return request.method == "GET" or (
            request.user.is_authenticated
            and request.method in self.write_allow_methods
        )

    def has_object_permission(self, request, view, obj):
        return (request.method == "GET") or (
            obj.author == request.user or request.user.is_superuser
        )
