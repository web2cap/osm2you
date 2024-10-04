import pytest
from core.models.markers import MarkerCluster
from django.contrib.gis.geos import Point


@pytest.fixture
def simple_marker_cluster_data():
    return {"location": Point(1, 2), "square_size": 3, "markers_count": 4}


@pytest.fixture
def simple_marker_cluster(simple_marker_cluster_data):
    return MarkerCluster.objects.create(**simple_marker_cluster_data)
