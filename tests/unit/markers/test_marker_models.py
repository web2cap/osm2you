import pytest
from django.db.utils import IntegrityError
from markers.models import Marker


class TestMarkersModels:
    @pytest.mark.django_db
    def test_create_marker(self, marker_with_author_data):
        """Test for creating marker."""

        marker = Marker.objects.create(**marker_with_author_data)
        assert (
            marker.name == marker_with_author_data["name"]
        ), "Created marker has wrong name"
        assert (
            marker.location == marker_with_author_data["location"]
        ), "Created marker has wrong location"
        assert (
            marker.author == marker_with_author_data["author"]
        ), "Created marker has wrong author"
        assert marker.add_date, "Created marker hasn't add_date"

    @pytest.mark.django_db
    def test_create_marker_none_name(self, simple_marker_data):
        """Test creating a marker with no name."""

        marker = Marker.objects.create(
            name=None, location=simple_marker_data["location"]
        )
        assert marker.name is None, "Created marker has not None name"

    @pytest.mark.django_db
    def test_create_marker_no_location(self, simple_marker_data):
        """Test creating a marker with no location."""

        with pytest.raises(IntegrityError):
            marker = Marker.objects.create(name=simple_marker_data["name"])
            marker.save()
