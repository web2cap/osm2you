from django.shortcuts import get_object_or_404

from core.models.users import User


class UserService:

    @staticmethod
    def get_by_username(username):
        return get_object_or_404(User, username=username)
