import pytest

from api.permissions import (
    AuthorAdminOrInstanceOnly,
    AuthorAdminOrReadOnly,
    CurrentUserGetPut,
    DenyAll,
)


class TestPermissions:
    # SERVICE
    def check_permissions(
        self,
        permission_class,
        request_instance,
        view_instance,
        request_method=None,
        view_action=None,
        obj_instance=None,
    ):
        permission_instance = permission_class()
        if request_method:
            request_instance.method = request_method
        if view_action:
            view_instance.action = view_action

        if obj_instance and not permission_instance.has_object_permission(
            request_instance,
            view_instance,
            obj_instance,
        ):
            return False

        return permission_instance.has_permission(request_instance, view_instance)

    # DenyAll
    @pytest.mark.django_db
    def test_deny_all(self, anonim_request, user_request, simple_view):
        """Test that user and anonim user hasn't permission if DenyAll."""

        deny_all_permission = DenyAll()
        assert not deny_all_permission.has_permission(anonim_request, simple_view), (
            "Anonim has permission when DenyAll class"
        )
        assert not deny_all_permission.has_permission(user_request, simple_view), (
            "User has permission when DenyAll class"
        )

    # CurrentUserGetPut
    @pytest.mark.parametrize(
        "request_method, expected_result",
        [
            ("GET", False),
            ("PUT", False),
            ("PATCH", False),
        ],
    )
    @pytest.mark.django_db
    def test_current_user_get_put_permission_anonim(
        self,
        simple_view,
        anonim_request,
        user_owner_instance,
        request_method,
        expected_result,
    ):
        """Test that anonim hasn't permissions to owner user instance if CurrentUserGetPut."""

        assert (
            self.check_permissions(
                CurrentUserGetPut,
                anonim_request,
                simple_view,
                request_method=request_method,
                obj_instance=user_owner_instance,
            )
            == expected_result
        ), f"Anonim has wrong permission to {request_method}."

    @pytest.mark.parametrize(
        "request_method, expected_result",
        [
            ("GET", False),
            ("PUT", False),
            ("PATCH", False),
        ],
    )
    @pytest.mark.django_db
    def test_current_user_get_put_permission_user(
        self,
        simple_view,
        user_request,
        user_owner_instance,
        request_method,
        expected_result,
    ):
        """Test that user hasn't permissions to other user instance if CurrentUserGetPut."""

        assert (
            self.check_permissions(
                CurrentUserGetPut,
                user_request,
                simple_view,
                request_method=request_method,
                obj_instance=user_owner_instance,
            )
            == expected_result
        ), f"Other user has wrong permission to {request_method}."

    @pytest.mark.parametrize(
        "request_method, expected_result",
        [
            ("GET", True),
            ("PUT", True),
            ("PATCH", False),
        ],
    )
    @pytest.mark.django_db
    def test_current_user_get_put_permission_owner(
        self,
        simple_view,
        owner_request,
        user_owner_instance,
        request_method,
        expected_result,
    ):
        """Test that owner has permissions to self instance if CurrentUserGetPut."""

        assert (
            self.check_permissions(
                CurrentUserGetPut,
                owner_request,
                simple_view,
                request_method=request_method,
                obj_instance=user_owner_instance,
            )
            == expected_result
        ), f"Owner has wrong permission to {request_method}."

    # AuthorAdminOrReadOnly
    @pytest.mark.parametrize(
        "request_method, expected_result",
        [
            ("GET", True),
            ("POST", True),
            ("PUT", False),
            ("PATCH", True),
            ("DELETE", True),
        ],
    )
    @pytest.mark.django_db
    def test_author_admin_or_read_only_admin(
        self,
        simple_marker,
        superuser_request,
        simple_view,
        request_method,
        expected_result,
    ):
        """Test that admin can POST, PATCH, DELETE and GET
        for AuthorAdminOrReadOnly permission."""

        simple_marker.author = superuser_request.user

        assert (
            self.check_permissions(
                AuthorAdminOrReadOnly,
                superuser_request,
                simple_view,
                request_method=request_method,
                obj_instance=simple_marker,
            )
            == expected_result
        ), f"Admin has wrong permission to {request_method} in AuthorAdminOrReadOnly."

    @pytest.mark.parametrize(
        "request_method, expected_result",
        [
            ("GET", True),
            ("POST", True),
            ("PUT", False),
            ("PATCH", True),
            ("DELETE", True),
        ],
    )
    @pytest.mark.django_db
    def test_author_admin_or_read_only_owner(
        self,
        simple_marker,
        owner_request,
        simple_view,
        request_method,
        expected_result,
    ):
        """Test that owner user can POST, PATCH, DELETE and GET
        for AuthorAdminOrReadOnly permission."""

        simple_marker.author = owner_request.user

        assert (
            self.check_permissions(
                AuthorAdminOrReadOnly,
                owner_request,
                simple_view,
                request_method=request_method,
                obj_instance=simple_marker,
            )
            == expected_result
        ), f"Owner has wrong permission to {request_method} in AuthorAdminOrReadOnly."

    @pytest.mark.parametrize(
        "request_method, expected_result",
        [
            ("GET", True),
            ("POST", False),
            ("PUT", False),
            ("PATCH", False),
            ("DELETE", False),
        ],
    )
    @pytest.mark.django_db
    def test_author_admin_or_read_only_user(
        self,
        simple_marker,
        user_request,
        user_owner_instance,
        simple_view,
        request_method,
        expected_result,
    ):
        """Test that user, not the owner can GET only
        for AuthorAdminOrReadOnly permission."""

        simple_marker.author = user_owner_instance

        assert (
            self.check_permissions(
                AuthorAdminOrReadOnly,
                user_request,
                simple_view,
                request_method=request_method,
                obj_instance=simple_marker,
            )
            == expected_result
        ), (
            f"Regular user has wrong permission to {request_method} in AuthorAdminOrReadOnly."
        )

    @pytest.mark.parametrize(
        "request_method, expected_result",
        [
            ("GET", True),
            ("POST", False),
            ("PUT", False),
            ("PATCH", False),
            ("DELETE", False),
        ],
    )
    @pytest.mark.django_db
    def test_author_admin_or_read_only_anonim(
        self,
        simple_marker,
        anonim_request,
        user_owner_instance,
        simple_view,
        request_method,
        expected_result,
    ):
        """Test that anonim can GET only
        for AuthorAdminOrReadOnly permission."""

        simple_marker.author = user_owner_instance

        assert (
            self.check_permissions(
                AuthorAdminOrReadOnly,
                anonim_request,
                simple_view,
                request_method=request_method,
                obj_instance=simple_marker,
            )
            == expected_result
        ), f"Anonim has wrong permission to {request_method} in AuthorAdminOrReadOnly."

    # AuthorAdminOrInstanceOnly
    @pytest.mark.parametrize(
        "request_method, view_action, expected_result",
        [
            ("GET", "list", False),
            ("GET", "retrieve", True),
            ("POST", "create", True),
            ("PUT", "update", False),
            ("PATCH", "partial_update", True),
            ("DELETE", "destroy", True),
        ],
    )
    @pytest.mark.django_db
    def test_author_admin_or_instance_only_admin(
        self,
        simple_marker,
        superuser_request,
        user_owner_instance,
        simple_view,
        request_method,
        view_action,
        expected_result,
    ):
        """Test that admin can retrive action or POST, PATCH, DELETE methods,
        for AuthorAdminOrInstanceOnly permission."""

        simple_marker.author = user_owner_instance
        assert (
            self.check_permissions(
                AuthorAdminOrInstanceOnly,
                superuser_request,
                simple_view,
                request_method=request_method,
                view_action=view_action,
                obj_instance=simple_marker,
            )
            == expected_result
        ), (
            f"Admin has wrong permission to {request_method} {view_action} in AuthorAdminOrReadOnly."
        )

    @pytest.mark.parametrize(
        "request_method, view_action, expected_result",
        [
            ("GET", "list", False),
            ("GET", "retrieve", True),
            ("POST", "create", True),
            ("PUT", "update", False),
            ("PATCH", "partial_update", True),
            ("DELETE", "destroy", True),
        ],
    )
    @pytest.mark.django_db
    def test_author_admin_or_instance_only_owner(
        self,
        simple_marker,
        owner_request,
        user_owner_instance,
        simple_view,
        request_method,
        view_action,
        expected_result,
    ):
        """Test that owner user can retrive action or POST, PATCH, DELETE methods,
        for AuthorAdminOrInstanceOnly permission."""

        simple_marker.author = user_owner_instance
        assert (
            self.check_permissions(
                AuthorAdminOrInstanceOnly,
                owner_request,
                simple_view,
                request_method=request_method,
                view_action=view_action,
                obj_instance=simple_marker,
            )
            == expected_result
        ), (
            f"Owner has wrong permission to {request_method} {view_action} in AuthorAdminOrReadOnly."
        )

    @pytest.mark.parametrize(
        "request_method, view_action, expected_result",
        [
            ("GET", "list", False),
            ("GET", "retrieve", True),
            ("POST", "create", False),
            ("PUT", "update", False),
            ("PATCH", "partial_update", False),
            ("DELETE", "destroy", False),
        ],
    )
    @pytest.mark.django_db
    def test_author_admin_or_instance_only_user(
        self,
        simple_marker,
        user_request,
        user_owner_instance,
        simple_view,
        request_method,
        view_action,
        expected_result,
    ):
        """Test that regular user can retrive action only,
        for AuthorAdminOrInstanceOnly permission."""

        simple_marker.author = user_owner_instance
        assert (
            self.check_permissions(
                AuthorAdminOrInstanceOnly,
                user_request,
                simple_view,
                request_method=request_method,
                view_action=view_action,
                obj_instance=simple_marker,
            )
            == expected_result
        ), (
            f"User has wrong permission to {request_method} {view_action} in AuthorAdminOrReadOnly."
        )

    @pytest.mark.parametrize(
        "request_method, view_action, expected_result",
        [
            ("GET", "list", False),
            ("GET", "retrieve", True),
            ("POST", "create", False),
            ("PUT", "update", False),
            ("PATCH", "partial_update", False),
            ("DELETE", "destroy", False),
        ],
    )
    @pytest.mark.django_db
    def test_author_admin_or_instance_only_anonim(
        self,
        simple_marker,
        anonim_request,
        user_owner_instance,
        simple_view,
        request_method,
        view_action,
        expected_result,
    ):
        """Test that anonim can retrive action only,
        for AuthorAdminOrInstanceOnly permission."""

        simple_marker.author = user_owner_instance
        assert (
            self.check_permissions(
                AuthorAdminOrInstanceOnly,
                anonim_request,
                simple_view,
                request_method=request_method,
                view_action=view_action,
                obj_instance=simple_marker,
            )
            == expected_result
        ), (
            f"Anonim has wrong permission to {request_method} {view_action} in AuthorAdminOrReadOnly."
        )
