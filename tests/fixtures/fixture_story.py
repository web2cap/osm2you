import pytest
from api.viewsets import StoryViewSet
from stories.models import Story


@pytest.fixture
def simple_story_data(user_owner_instance):
    return {
        "text": "Story simle text",
        "author": user_owner_instance,
    }


@pytest.fixture
def story_with_marker_data(simple_story_data, simple_marker):
    return simple_story_data | {"marker": simple_marker}


@pytest.fixture
def second_story_data_user(user_instance):
    return {
        "text": "Second story simle text",
        "author": user_instance,
    }


@pytest.fixture
def second_story_for_marker_author_user(
    marker_with_author_story, second_story_data_user
):
    """Adds a secont story with different author for marker_with_author_data."""
    return Story.objects.create(
        marker=marker_with_author_story, **second_story_data_user
    )


@pytest.fixture
def story_viewset():
    return StoryViewSet()


@pytest.fixture
def simple_story(simple_marker, simple_story_data):
    return Story.objects.create(marker=simple_marker, **simple_story_data)
