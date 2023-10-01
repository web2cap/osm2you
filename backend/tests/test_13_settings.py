# from ..mymap import settings
from django.conf import settings


class TestSettings:
    def test_settings(self):
        print(f"settings.DEBUG: {settings.DEBUG}")
        assert (
            not settings.DEBUG
        ), "Check that DEBUG is disabled in Django settings"
        assert (
            settings.DATABASES["default"]["ENGINE"]
            == "django.contrib.gis.db.backends.postgis"
        ), "Check you are using postgresql database"
