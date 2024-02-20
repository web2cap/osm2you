import pytest
from core.admin.markers import MarkerAdmin
from core.models.markers import Marker
from django.contrib.gis import admin


class TestMarkerAdmin:
    def test_marker_registration_in_admin(self):
        assert (
            Marker in admin.site._registry
        ), "Marker model should be registered in admin site"

    def test_marker_admin_inherits_from_user_admin(self):
        assert issubclass(
            MarkerAdmin, admin.GISModelAdmin
        ), "MarkerAdmin should inherit from GISModelAdmin"

    @pytest.mark.django_db
    def test_marker_admin_get_form(self, user_request):
        marker_admin = MarkerAdmin(Marker, admin.site)
        marker_admin_form = marker_admin.get_form(user_request)
        assert (
            marker_admin_form.base_fields["author"].initial == user_request.user.id
        ), "Get admin form doesn't add user id to author."
