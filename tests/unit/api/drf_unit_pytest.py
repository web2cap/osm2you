from abc import ABC, abstractmethod

import pytest


@pytest.fixture
def simple_instance():
    pass


@pytest.fixture
def simple_json():
    pass


class AbstractTestSerializer(ABC):
    @property
    @abstractmethod
    def serializer_class(self):
        """Subclasses must define serializer."""
        pass

    @property
    @abstractmethod
    def fields_must_present(self):
        """Subclasses must define list of fields, which must present in response."""
        pass

    @abstractmethod
    def fields_must_equal(self, simple_instance):
        """Subclasses must return dict of fields, with expected values."""
        pass

    @property
    def read_only_serializer(self):
        """Subclasses must define read_only_serializer property to False
        if serializer only for safe methods."""
        return False

    @pytest.mark.django_db
    def test_serializer_valid(self, simple_json):
        """Check serialization with valid data."""

        if self.read_only_serializer:
            return
        serializer = self.serializer_class(data=simple_json)
        assert (
            serializer.is_valid()
        ), f"Error serialize with valid data {serializer.errors}"

    @pytest.mark.django_db
    def test_serializer_data_present(self, simple_instance):
        """Check that needet data includet."""

        serializer = self.serializer_class(instance=simple_instance)

        for must_present in self.fields_must_present:
            assert (
                must_present in serializer.data
            ), f"Field {must_present} should present in valid data."

    @pytest.mark.django_db
    def test_serializer_data_equal(self, simple_instance):
        serializer = self.serializer_class(instance=simple_instance)
        fields_must_equal = self.fields_must_equal(simple_instance)

        for field in fields_must_equal:
            assert (
                serializer.data[field] == fields_must_equal[field]
            ), f"{field} in serialized data not eqal user model data"

    @pytest.mark.django_db
    def test_serializer_excludet_data(self, simple_instance):
        """Check that no extra fields includet."""

        serializer = self.serializer_class(instance=simple_instance)
        for field in simple_instance._meta.fields:
            assert (
                field.name in self.fields_must_present
                or field.name not in serializer.data
            ), f"Field {field.name} should not present in valid data."
