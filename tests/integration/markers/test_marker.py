import pytest

from ..common import check_response


class TestMarker:
    URL_MARKERS = "/api/v1/markers/"

    # GET LIST
    def check_marker_list(self, client, marker):
        """Tests a request against a list of markers.
        Checks the number of markers in the list.
        Checking the fields and field values of one marker in the list.
        Returns the response element of a single marker for detailed checking."""

        response = client.get(self.URL_MARKERS)
        required_fields = ["type", "features"]
        check_response(response, 200, required_fields)

        assert len(response.data["features"]) == 2, "Response must has 2 markers"

        response_simple_marker = next(
            (
                feature
                for feature in response.data["features"]
                if feature["id"] == marker.id
            ),
            None,
        )
        assert response_simple_marker, "No expected marker in response."

        assert (
            "type" in response_simple_marker
            and response_simple_marker["type"] == "Feature"
        ), "Wrong type in marker list response"
        assert (
            "geometry" in response_simple_marker
        ), "No geometry in marker list response"
        assert (
            "type" in response_simple_marker["geometry"]
            and response_simple_marker["geometry"]["type"] == "Point"
        ), "Wrong geometry type in marker list response"
        assert "coordinates" in response_simple_marker[
            "geometry"
        ] and response_simple_marker["geometry"]["coordinates"] == [
            marker.location.x,
            marker.location.y,
        ], "Wrong geometry coordinates in marker list response"
        assert (
            "properties" in response_simple_marker
        ), "No properties in marker list response"
        assert (
            "name" in response_simple_marker["properties"]
            and response_simple_marker["properties"]["name"] == marker.name
        ), "Wrong name in marker list response"

        return response_simple_marker

    @pytest.mark.django_db()
    def test_marker_list_unauthorized(
        self, client, simple_marker, marker_with_author_story
    ):
        """Tests unauthorized request to marker list.
        Checks that in response is_yours is false."""

        response_simple_marker = self.check_marker_list(client, simple_marker)
        assert (
            "is_yours" in response_simple_marker["properties"]
            and response_simple_marker["properties"]["is_yours"] is False
        ), "is_yours can't be true in unauthorized marker list response"

    @pytest.mark.django_db()
    def test_marker_list_authorized(
        self, use_owner_client, user_client, simple_marker, marker_with_author_story
    ):
        """Tests authorized request to marker list.
        Checks that in response is_yours eqal true for marker,
        which author and client user is same.
        Checks that in response is_yours eqal false for marker,
        which author and client user is different.
        """

        response_marker_with_author_story = self.check_marker_list(
            use_owner_client, marker_with_author_story
        )
        assert (
            "is_yours" in response_marker_with_author_story["properties"]
            and response_marker_with_author_story["properties"]["is_yours"] is True
        ), "is_yours must be true in authorized marker list response for this marker"

        response_marker_with_author_story = self.check_marker_list(
            user_client, marker_with_author_story
        )
        assert (
            "is_yours" in response_marker_with_author_story["properties"]
            and response_marker_with_author_story["properties"]["is_yours"] is False
        ), "is_yours must be false in authorized marker list response for this marker"
