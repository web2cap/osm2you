import pytest
from abc_serializer_test import AbstractTestSerializer
from api.serializers import (
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


class AbstractTestMarkerSerializer(AbstractTestSerializer):
    """Abstract class with extra tests for marker serializer."""

    @property
    def fields_must_present(self):
        return ["id", "type", "geometry", "properties"]

    def expected_data(self, simple_instance):
        return {
            "id": simple_instance.id,
        }

    @pytest.mark.django_db
    def test_serializer_data_type_field(self, simple_instance):
        """Check that type field data is correct."""

        serializer = self.serializer_class(instance=simple_instance)
        assert (
            serializer.data["type"] == "Feature"
        ), "Field type should be equal Feature."

    @pytest.mark.django_db
    def test_serializer_data_geometry(self, simple_instance):
        """Check that  geometry is correct."""

        serializer = self.serializer_class(instance=simple_instance)

        assert (
            "type" in serializer.data["geometry"]
        ), "Field geometry.type should be present in valid data."
        assert (
            serializer.data["geometry"]["type"] == "Point"
        ), "Field type should be equal Point."

        assert (
            "coordinates" in serializer.data["geometry"]
        ), "Field geometry.type should be present in valid data."
        assert serializer.data["geometry"]["coordinates"] == [
            simple_instance.location.x,
            simple_instance.location.y,
        ], "Field coordinates should be equal marker location coordinates."

    @pytest.mark.django_db
    def test_serializer_data_properties(self, simple_instance):
        """Check that properties is correct."""

        serializer = self.serializer_class(instance=simple_instance)

        assert (
            "name" in serializer.data["properties"]
        ), "Field properties.name should be present in valid data."
        assert (
            serializer.data["properties"]["name"] == simple_instance.name
        ), "Field properties.name should be equal instance name."


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
