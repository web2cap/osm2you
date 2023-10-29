import pytest
from django.urls import resolve


class TestMymapUrls:
    @pytest.mark.parametrize(
        "url, view_name",
        [
            ("/api/v1/markers/", "api:markers-list"),
            ("/api/v1/stories/", "api:stories-list"),
            ("/api/v1/auth/", "api:api-root"),
            ("/api/v1/auth/jwt/create/", "api:jwt-create"),
            ("/api/v1/docs/", "api:docs"),
            ("/api/v1/redoc/", "api:redoc"),
        ],
    )
    def test_url(self, url, view_name):
        """Test a URL pattern in urlpatterns."""

        url_pattern = resolve(url)
        assert url_pattern, f"URL pattern for '{url}' not found"
        assert (
            url_pattern.view_name == view_name
        ), f"View '{view_name}' in pattern for '{url}' not found"
