import pytest

from django.urls import resolve


class TestMymapUrls:
    @pytest.mark.parametrize(
        "url, view_name",
        [
            ("/admin/", "admin:index"),
            ("/api/v1/", "api:api-root"),
        ],
    )
    def test_url(self, url, view_name):
        """Test a URL pattern in urlpatterns."""

        url_pattern = resolve(url)
        assert url_pattern, f"URL pattern for '{url}' not found"
        assert (
            url_pattern.view_name == view_name
        ), f"View '{view_name}' in pattern for '{url}' not found"
