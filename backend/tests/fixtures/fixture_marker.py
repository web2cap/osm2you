import pytest
from django.contrib.gis.geos import Point

from markers.models import Marker


@pytest.fixture
def simple_marker():
    return Marker.objects.create(name="Simple marker", location=Point(1, 1))
