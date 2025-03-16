import pytest
from core.models.tags import Tag
from django.db.utils import IntegrityError


class TestTagModels:
    @pytest.mark.django_db
    def test_create_tag(self, simple_tag_data):
        """Test for creating tag."""

        tag = Tag.objects.create(**simple_tag_data)
        assert tag.name == simple_tag_data["name"], "Created tag has wrong name"
        assert tag.display_name == simple_tag_data["display_name"], (
            "Created tag has wrong display_name"
        )
        assert tag.created, "Created tag has no created value"

    @pytest.mark.django_db
    def test_create_tag_no_name(self, simple_tag_data):
        """Test creating a tag with no name."""

        simple_tag_data.pop("name")
        with pytest.raises(IntegrityError):
            tag = Tag.objects.create(**simple_tag_data)
            tag.save()

    @pytest.mark.django_db
    def test_create_tag_no_display_name(self, simple_tag_data):
        """Test for creating tag without display_name."""

        simple_tag_data.pop("display_name")
        tag = Tag.objects.create(**simple_tag_data)
        assert tag.name == simple_tag_data["name"], "Created tag has wrong name"
        assert not tag.display_name, "Created tag should has not display_name"
        assert tag.created, "Created tag has no created value"
