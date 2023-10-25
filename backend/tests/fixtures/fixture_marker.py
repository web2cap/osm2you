import pytest
from django.contrib.gis.geos import Point

from api.viewsets import MarkerViewSet
from markers.models import Marker


@pytest.fixture
def simple_marker_data():
    return {"name": "Simple marker", "location": Point(1, 1)}


@pytest.fixture
def simple_marker(simple_marker_data):
    return Marker.objects.create(**simple_marker_data)


@pytest.fixture
def marker_with_author_story(user_owner_instance, simple_story_data):
    marker = Marker.objects.create(
        name="Marker with stories", location=Point(1, 1), author=user_owner_instance
    )
    marker.stories.create(**simple_story_data)
    return marker


@pytest.fixture
def marker_viewset():
    return MarkerViewSet()


@pytest.fixture
def marker_viewset_instance_list():
    marker_viewset = MarkerViewSet()
    marker_viewset.action = "list"
    return marker_viewset


@pytest.fixture
def marker_viewset_instance_retrieve():
    marker_viewset = MarkerViewSet()
    marker_viewset.action = "retrieve"
    return marker_viewset
