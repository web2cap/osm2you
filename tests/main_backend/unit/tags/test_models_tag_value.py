import pytest
from core.models.tag_values import TagValue
from django.db.utils import IntegrityError


class TestTagValueModels:
    @pytest.mark.django_db
    def test_create_tag(self, simple_tag_value_data):
        """Test for creating Tag value."""

        tag = TagValue.objects.create(**simple_tag_value_data)
        assert tag.value == simple_tag_value_data["value"], (
            "Created tag has wrong value"
        )
        assert tag.marker == simple_tag_value_data["marker"], (
            "Created tag has wrong marker"
        )
        assert tag.tag == simple_tag_value_data["tag"], (
            "Created tag has wrong tag relation"
        )
        assert tag.created, "Created tag has no created value"

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "blank_field",
        ["tag", "marker"],
    )
    def test_tag_value_create_blank_field(self, simple_tag_value_data, blank_field):
        """Test creating a tag with no value."""

        simple_tag_value_data.pop(blank_field)
        with pytest.raises(IntegrityError):
            tag = TagValue.objects.create(**simple_tag_value_data)
            tag.save()

    @pytest.mark.django_db()
    def test_tag_value_create_non_unic(self, simple_tag_value_data):
        """Test creating a tag with no value."""

        with pytest.raises(IntegrityError):
            tag = TagValue.objects.create(**simple_tag_value_data)
            tag.save()
            tag = TagValue.objects.create(**simple_tag_value_data)
            tag.save()
