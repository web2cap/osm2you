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
def story_viewset():
    return StoryViewSet()


@pytest.fixture
def simple_story(simple_marker, simple_story_data):
    return Story.objects.create(marker=simple_marker, **simple_story_data)
