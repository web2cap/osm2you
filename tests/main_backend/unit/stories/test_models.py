import pytest
from core.models.stories import Story
from django.db.utils import IntegrityError


class TestStoriesModels:
    @pytest.mark.django_db
    def test_create_story(self, story_with_marker_data):
        """Test for creating story."""

        story = Story.objects.create(**story_with_marker_data)
        assert (
            story.text == story_with_marker_data["text"]
        ), "Created story has wrong text"
        assert (
            story.author == story_with_marker_data["author"]
        ), "Created story has wrong author"
        assert (
            story.marker == story_with_marker_data["marker"]
        ), "Created story has wrong marker"

    @pytest.mark.django_db
    def test_create_marker_no_text(self, story_with_marker_data):
        """Test creating a story with no text."""

        story_with_marker_data.pop("text")
        with pytest.raises(IntegrityError):
            story = Story.objects.create(**story_with_marker_data)
            story.save()

    @pytest.mark.django_db
    def test_create_marker_no_marker(self, simple_story_data):
        """Test creating a story with no marker."""

        with pytest.raises(IntegrityError):
            story = Story.objects.create(**simple_story_data)
            story.save()
