from core.models.tags import Tag
from django.contrib.gis import admin


class TestTagAdmin:
    def test_story_registration_in_admin(self):
        assert Tag in admin.site._registry, (
            "Tag model should be registered in admin site"
        )
