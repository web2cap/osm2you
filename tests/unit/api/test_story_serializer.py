import pytest
from abc_serializer_test import AbstractTestSerializer
from api.serializers import StorySerializer, StorySerializerDisplay


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


class TestStorySerializerDisplay(AbstractTestSerializer):
    @property
    def serializer_class(self):
        return StorySerializerDisplay

    @property
    def fields_must_present(self):
        return ["id", "text", "author", "is_yours"]

    def expected_data(self, simple_instance):
        return {
            "id": simple_instance.id,
            "text": simple_instance.text,
        }

    @property
    def read_only_serializer(self):
        return True

    @pytest.mark.django_db
    def test_serializer_author_data_present(self, simple_instance):
        """Check that required data is included in the serialized output."""

        serializer = self.serializer_class(instance=simple_instance)

        author_fields_must_present = ["id", "first_name", "username"]
        for must_present in author_fields_must_present:
            assert (
                must_present in serializer.data["author"]
            ), f"Field {must_present} should be present in valid author data."

    @pytest.mark.django_db
    def test_serializer_data_equal(self, simple_instance, user_owner_instance):
        serializer = self.serializer_class(instance=simple_instance)
        assert (
            serializer.data["author"]["id"] == user_owner_instance.id
        ), "Author id in serialized data does not match the expected value."
        assert (
            serializer.data["author"]["first_name"] == user_owner_instance.first_name
        ), "Author first_name in serialized data does not match the expected value."
        assert (
            serializer.data["author"]["username"] == user_owner_instance.username
        ), "Author username in serialized data does not match the expected value."
