import pytest
from abc_serializer_test import AbstractTestSerializer
from api.serializers import MarkerSerializer


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
