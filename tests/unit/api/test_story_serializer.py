import pytest
from api.serializers import StorySerializer
from drf_unit_pytest import AbstractTestSerializer


@pytest.fixture
def simple_instance(simple_story, simple_marker, user_owner_instance):
    return simple_story


@pytest.fixture
def simple_json(simple_story_json, simple_marker):
    return simple_story_json


class TestStorySerializer(AbstractTestSerializer):
    @property
    def serializer_class(self):
        return StorySerializer

    @property
    def fields_must_present(self):
        return ["id", "text", "author", "marker"]

    def fields_must_equal(self, simple_instance):
        return {
            "text": simple_instance.text,
            "author": simple_instance.author.id,
            "marker": simple_instance.marker.id,
        }
