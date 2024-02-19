from django.contrib.gis import admin
from tags.models import Tag


class TestTagAdmin:
    def test_story_registration_in_admin(self):
        assert (
            Tag in admin.site._registry
        ), "Tag model should be registered in admin site"
