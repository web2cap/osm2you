import pytest


@pytest.fixture
def simple_story_data(user_owner_instance):
    return {
        "text": "Story simle text",
        "author": user_owner_instance,
    }
