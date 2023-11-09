import pytest
from abc_serializer_test import AbstractTestSerializer
from api.serializers import StorySerializer


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

    def expected_data(self, simple_instance):
        return {
            "text": simple_instance.text,
            "author": simple_instance.author.id,
            "marker": simple_instance.marker.id,
        }

    @pytest.mark.django_db
    def test_serializer_short_text(self, simple_story_json):
        """Check that serializer rise error if text less 10 ch."""

        simple_story_json["text"] = simple_story_json["text"][:8]
        serializer = self.serializer_class(data=simple_story_json)
        assert (
            not serializer.is_valid()
        ), "Serializer must rise the error if text len is less 10"
