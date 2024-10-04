from core.models.stories import Story
from django.contrib.gis import admin


class TestStoryAdmin:
    def test_story_registration_in_admin(self):
        assert (
            Story in admin.site._registry
        ), "Story model should be registered in admin site"
