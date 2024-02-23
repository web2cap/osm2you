import pytest
from abc_serializer_marker_test import AbstractTestMarkerSerializer
from api.serializers.markers import (
    MarkerInstanceSerializer,
    MarkerSerializer,
    MarkerUserSerializer,
)


@pytest.fixture
def simple_instance(marker_with_author_story):
    return marker_with_author_story


@pytest.fixture
def simple_json(simple_marker_json):
    return simple_marker_json


class TestMarkerSerializer(AbstractTestMarkerSerializer):
    """Tests default marker serializer."""

    @property
    def serializer_class(self):
        return MarkerSerializer

    @pytest.mark.django_db
    def test_serializer_data_is_yours(self, simple_instance):
        """Check that properties.is_yours is correct."""

        serializer = self.serializer_class(instance=simple_instance)

        assert (
            "is_yours" in serializer.data["properties"]
        ), "Field properties.is_yours should be present in valid data."
        assert (
            serializer.data["properties"]["is_yours"] is False
        ), "Field properties.is_yours should be equal False."


class TestMarkerInstanceSerializer(TestMarkerSerializer):
    """Tests marker instance serializer with stories and stories author."""

    @property
    def serializer_class(self):
        return MarkerInstanceSerializer

    @pytest.mark.django_db
    def test_serializer_data_properties_stories(self, simple_instance):
        """Check that properties stories is correct."""

        serializer = self.serializer_class(instance=simple_instance)

        assert (
            "stories" in serializer.data["properties"]
        ), "Field properties.stories should be present in valid data."

        assert len(
            serializer.data["properties"]["stories"]
        ), "properties.stories.id should content elemet."

        serializer_story = serializer.data["properties"]["stories"][0]
        isinstance_story = simple_instance.stories.first()

        assert (
            "id" in serializer_story
        ), "Field properties.stories.id should be present in valid data."
        assert (
            serializer_story["id"] == isinstance_story.id
        ), "Field properties.stories.id should be equal instance stories.id."

        assert (
            "text" in serializer_story
        ), "Field properties.stories.text should be present in valid data."
        assert (
            serializer_story["text"] == isinstance_story.text
        ), "Field properties.stories.text should be equal instance stories.text."

        assert (
            "is_yours" in serializer_story
        ), "Field properties.stories.is_yours should be present in valid data."
        assert (
            serializer_story["is_yours"] is False
        ), "Field properties.stories.is_yours should be equal False."

    @pytest.mark.django_db
    def test_serializer_data_properties_stories_author(self, simple_instance):
        """Check that properties stories author is correct."""

        serializer = self.serializer_class(instance=simple_instance)

        assert (
            "author" in serializer.data["properties"]["stories"][0]
        ), "Field properties.stories.author should be present in valid data."

        serializer_story_author = serializer.data["properties"]["stories"][0]["author"]
        isinstance_story_author = simple_instance.stories.first().author

        assert (
            "id" in serializer_story_author
        ), "Field properties.stories.author.id should be present in valid data."
        assert (
            serializer_story_author["id"] == isinstance_story_author.id
        ), "Field properties.stories.author.id should be equal instance stories.author.id."

        assert (
            "first_name" in serializer_story_author
        ), "Field properties.stories.author.first_name should be present in valid data."
        assert (
            serializer_story_author["first_name"] == isinstance_story_author.first_name
        ), "Field properties.stories.author.first_name should be equal instance stories.author.first_name."

        assert (
            "username" in serializer_story_author
        ), "Field properties.stories.author.username should be present in valid data."
        assert (
            serializer_story_author["username"] == isinstance_story_author.username
        ), "Field properties.stories.author.username should be equal instance stories.author.username."

    @pytest.mark.django_db
    def test_serializer_data_properties_tags(self, marker_with_tag):
        """Check that properties tags is correct."""

        serializer = self.serializer_class(instance=marker_with_tag)

        assert (
            "tags" in serializer.data["properties"]
        ), "Field properties.tags should be present in valid data."

        assert len(
            serializer.data["properties"]["tags"]
        ), "properties.tags should content elemet."

        isinstance_tag_value = marker_with_tag.tag_value.first()

        assert (
            isinstance_tag_value.tag.name in serializer.data["properties"]["tags"]
        ), "Key properties.tags should be present in valid data."
        assert (
            serializer.data["properties"]["tags"][isinstance_tag_value.tag.name]
            == isinstance_tag_value.value
        ), "Field properties.tags.value should be equal instance value."

    @pytest.mark.django_db
    def test_serializer_data_properties_add_date(self, simple_instance):
        """Check that properties add_date is correct."""

        serializer = self.serializer_class(instance=simple_instance)

        assert (
            "add_date" in serializer.data["properties"]
        ), "Field properties.add_date should be present in valid data."
        assert serializer.data["properties"][
            "add_date"
        ] == simple_instance.add_date.strftime(
            "%Y-%m-%dT%H:%M:%S.%f"
        ), "Wrong add_date in marker serialized data"


class TestMarkerUserSerializer(AbstractTestMarkerSerializer):
    """Tests users marker serializer with stories."""

    @property
    def serializer_class(self):
        return MarkerUserSerializer

    @pytest.mark.django_db
    def test_serializer_data_properties_stories(self, simple_instance):
        """Check that properties stories is correct."""

        serializer = self.serializer_class(instance=simple_instance)

        assert (
            "stories" in serializer.data["properties"]
        ), "Field properties.stories should be present in valid data."

        assert len(
            serializer.data["properties"]["stories"]
        ), "properties.stories.id should content elemet."

        assert (
            "text" in serializer.data["properties"]["stories"][0]
        ), "Field properties.stories.text should be present in valid data."
        assert (
            serializer.data["properties"]["stories"][0]["text"]
            == simple_instance.stories.first().text
        ), "Field properties.stories.text should be equal instance stories.text."
