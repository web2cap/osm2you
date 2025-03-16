import pytest


class TestStoryViewset:
    """Tests marker viewset."""

    @pytest.mark.django_db
    def test_get_queryset(
        self, story_viewset, simple_story, user_owner_instance, simple_marker
    ):
        """Test are story, marker, author in story queryset."""
        queryset = story_viewset.get_queryset()
        assert simple_story in queryset, "No story in story queryset"
        assert queryset.first().author == user_owner_instance, (
            "No story author in story queryset"
        )
        assert queryset.first().marker == simple_marker, (
            "No story marker in story queryset"
        )
