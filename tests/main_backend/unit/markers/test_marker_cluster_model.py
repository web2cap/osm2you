import pytest
from core.models.markers import MarkerCluster
from django.db.utils import IntegrityError


class TestMarkerClusterModels:
    @pytest.mark.django_db
    def test_create_marker_cluster(self, simple_marker_cluster_data):
        """Test for creating marker cluster."""

        marker_cluster = MarkerCluster.objects.create(**simple_marker_cluster_data)
        assert marker_cluster.location == simple_marker_cluster_data["location"], (
            "Created cluster has wrong location"
        )
        assert (
            marker_cluster.square_size == simple_marker_cluster_data["square_size"]
        ), "Created cluster has wrong zoom"
        assert marker_cluster.update_date, "Created cluster hasn't update_date"

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "required_field",
        ["location", "square_size", "markers_count"],
    )
    def test_create_marker_cluster_no_required(
        self, simple_marker_cluster_data, required_field
    ):
        """Test creating a marker cluster with no required field."""

        simple_marker_cluster_data.pop(required_field)
        with pytest.raises(IntegrityError):
            marker_cluster = MarkerCluster.objects.create(**simple_marker_cluster_data)
            marker_cluster.save()

    @pytest.mark.django_db
    def test_create_marker_cluster_negative_markers_count(
        self, simple_marker_cluster_data
    ):
        """Test creating a marker cluster with negative markers count."""

        simple_marker_cluster_data["markers_count"] = -1
        with pytest.raises(IntegrityError):
            marker_cluster = MarkerCluster.objects.create(**simple_marker_cluster_data)
            marker_cluster.save()
