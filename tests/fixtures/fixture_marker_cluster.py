import pytest
from django.contrib.gis.geos import Point
from markers.models import MarkerCluster


@pytest.fixture
def simple_marker_cluster_data():
    return {"location": Point(1, 2), "zoom": 3, "markers_count": 4}


@pytest.fixture
def simple_marker_cluster(simple_marker_cluster_data):
    return MarkerCluster.objects.create(**simple_marker_cluster_data)
