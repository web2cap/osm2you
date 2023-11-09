from abc import ABC, abstractmethod

import pytest


@pytest.fixture
def simple_instance():
    # Implement this fixture to provide a sample model instance for testing
    pass


@pytest.fixture
def simple_json():
    # Implement this fixture to provide valid JSON data for serializer testing
    pass


class AbstractTestSerializer(ABC):
    @property
    @abstractmethod
    def serializer_class(self):
        """Subclasses must define the serializer class."""
        pass

    @property
    @abstractmethod
    def fields_must_present(self):
        """Subclasses must define a list of fields that must be present in the response."""
        pass

    @abstractmethod
    def expected_data(self, simple_instance):
        """Subclasses must return a dictionary of fields with expected values.
        return example = {
            "text": simple_instance.text,
            "author": simple_instance.author.id,
        }."""
        pass

    @property
    def read_only_serializer(self):
        """Subclasses must define the read_only_serializer property to True
        if serializer is only for safe methods."""
        return False

    @pytest.mark.django_db
    def test_serializer_valid(self, simple_json):
        """Check serialization with valid data."""

        if self.read_only_serializer:
            return
        serializer = self.serializer_class(data=simple_json)
        assert (
            serializer.is_valid()
        ), f"Error serializing with valid data: {serializer.errors}"

    @pytest.mark.django_db
    def test_serializer_data_present(self, simple_instance):
        """Check that required data is included in the serialized output."""

        serializer = self.serializer_class(instance=simple_instance)

        for must_present in self.fields_must_present:
            assert (
                must_present in serializer.data
            ), f"Field {must_present} should be present in valid data."

    @pytest.mark.django_db
    def test_serializer_data_equal(self, simple_instance):
        serializer = self.serializer_class(instance=simple_instance)
        expected_data = self.expected_data(simple_instance)

        for field, expected_value in expected_data.items():
            assert (
                serializer.data[field] == expected_value
            ), f"{field} in serialized data does not match the expected value."

    @pytest.mark.django_db
    def test_serializer_excluded_data(self, simple_instance):
        """Check that no extra fields are included in the serialized output."""

        serializer = self.serializer_class(instance=simple_instance)
        for field in simple_instance._meta.fields:
            assert (
                field.name in self.fields_must_present
                or field.name not in serializer.data
            ), f"Field {field.name} should not be present in valid data."
