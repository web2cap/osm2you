import pytest
from api.viewsets.markers import MarkerViewSet
from core.models.markers import Marker
from core.services.bbox_square import BboxSquare
from django.conf import settings
from django.contrib.gis.geos import Point

CLUSTERING = getattr(settings, "CLUSTERING", {})
CLUSTERING_DENCITY = getattr(settings, "CLUSTERING_DENCITY", 36)


@pytest.fixture
def simple_marker_data():
    return {"name": "Simple marker", "location": Point(1, 2)}


@pytest.fixture
def simple_marker_json():
    return {
        "name": "Simple marker",
        "location": {"type": "Point", "coordinates": [1, 2]},
    }


@pytest.fixture
def simple_marker_updated_json():
    return {
        "name": "Updated Simple marker",
        "location": {"type": "Point", "coordinates": [10, 20]},
    }


@pytest.fixture
def marker_with_author_data(user_owner_instance):
    return {
        "name": "Marker with author",
        "location": Point(3, 4),
        "author": user_owner_instance,
    }


@pytest.fixture
def simple_marker_updated_json_same_location():
    return {"location": {"type": "Point", "coordinates": [1, 2]}}


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
def camp_site_marker_with_author_story(
    marker_with_author_story, camp_site_tag_value_data
):
    marker_with_author_story.tag_value.create(**camp_site_tag_value_data)
    return marker_with_author_story


@pytest.fixture
def marker_different_author_with_story_owner_story_user(
    user_instance, simple_story_data, second_story_data_user
):
    marker = Marker.objects.create(
        name="Marker by author user, with story by author owner",
        location=Point(4, 2),
        author=user_instance,
    )
    marker.stories.create(**simple_story_data)
    marker.stories.create(**second_story_data_user)
    return marker


@pytest.fixture
def marker_with_tag(user_owner_instance, simple_tagǜalue_withoutmarker_data):
    marker = Marker.objects.create(
        name="Marker with tag", location=Point(5, 5), author=user_owner_instance
    )
    marker.tag_value.create(**simple_tagǜalue_withoutmarker_data)
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
def marker_with_author_story_bbox(marker_with_author_story):
    """Calculates bbox with large zoom around marker_with_author_story."""
    indent = CLUSTERING["square_size"][0] / 2
    in_bbox = ",".join(
        map(
            str,
            (
                marker_with_author_story.location.x - indent,
                marker_with_author_story.location.y - indent,
                marker_with_author_story.location.x + indent,
                marker_with_author_story.location.y
                + indent
                + (CLUSTERING_DENCITY * 0.9),
            ),
        )
    )
    return in_bbox


@pytest.fixture
def marker_viewset_instance_list_large_zoom(marker_with_author_story_bbox):
    marker_viewset = MarkerViewSet()
    marker_viewset.action = "list"

    marker_viewset.bbox_square_service = BboxSquare(marker_with_author_story_bbox)
    return marker_viewset


@pytest.fixture
def marker_viewset_instance_list_small_zoom():
    marker_viewset = MarkerViewSet()
    marker_viewset.action = "list"
    marker_viewset.bbox_square_service = BboxSquare()
    return marker_viewset


@pytest.fixture
def marker_viewset_instance_retrieve():
    marker_viewset = MarkerViewSet()
    marker_viewset.action = "retrieve"
    return marker_viewset


@pytest.fixture
def marker_viewset_instance_user():
    marker_viewset = MarkerViewSet()
    marker_viewset.action = "user"
    return marker_viewset
