import pytest

from ..common import check_response


class TestMarker:
    URL_MARKERS = "/api/v1/markers/"

    # GET LIST
    def check_marker_list(self, client, marker):
        """Tests a request to markers list.
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
        self, user_owner_client, user_client, simple_marker, marker_with_author_story
    ):
        """Tests authorized request to marker list.
        Checks that in response is_yours eqal true for marker,
        which author and client user is same.
        Checks that in response is_yours eqal false for marker,
        which author and client user is different.
        """

        response_marker_with_author_story = self.check_marker_list(
            user_owner_client, marker_with_author_story
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

    # GET INSTANCE

    def check_marker_instance(self, client, marker, owner_instance, simple_story_data):
        """Tests a request to markers instance.
        Checking the fields and field values of marker in the list.
        Returns the response data of a marker for detailed checking and owner story response data
        """

        response = client.get(f"{self.URL_MARKERS}{marker.id}/")
        required_fields = ["id", "type", "geometry", "properties"]
        check_response(response, 200, required_fields)

        assert response.data["type"] == "Feature", "Wrong type in response"

        assert (
            "type" in response.data["geometry"]
            and response.data["geometry"]["type"] == "Point"
        ), "Wrong geometry type in marker response"
        assert "coordinates" in response.data["geometry"] and response.data["geometry"][
            "coordinates"
        ] == [
            marker.location.x,
            marker.location.y,
        ], "Wrong geometry coordinates in marker response"
        assert (
            "name" in response.data["properties"]
            and response.data["properties"]["name"] == marker.name
        ), "Wrong name in marker response"

        # Storise in marker
        assert "stories" in response.data["properties"], "No stories in marker response"
        assert (
            len(response.data["properties"]["stories"]) == 2
        ), "Stories in marker response must include 2 story"
        response_owner_story = next(
            (
                story
                for story in response.data["properties"]["stories"]
                if "author" in story
                and "id" in story["author"]
                and story["author"]["id"] == owner_instance.id
            ),
            None,
        )
        assert response_owner_story, "No expected story in response."
        assert (
            "id" in response_owner_story and response_owner_story["id"]
        ), "Wrong story id field"
        assert (
            "text" in response_owner_story and simple_story_data["text"]
        ), "Wrong story text field"
        assert (
            "first_name" in response_owner_story["author"]
            and response_owner_story["author"]["first_name"]
            == owner_instance.first_name
        ), "Wrong story author first_name field"
        assert (
            "username" in response_owner_story["author"]
            and response_owner_story["author"]["username"] == owner_instance.username
        ), "Wrong story author username field"

        return response.data, response_owner_story

    @pytest.mark.django_db()
    def test_marker_instance_unauthorized(
        self,
        client,
        marker_with_author_story,
        second_story_for_marker_author_user,
        user_owner_instance,
        simple_story_data,
    ):
        """Tests unauthorized request to marker instance.
        Checks that in response is_yours for marker is false.
        Checks that in response is_yours fro story is false."""

        response_marker, response_owner_story = self.check_marker_instance(
            client, marker_with_author_story, user_owner_instance, simple_story_data
        )
        assert (
            "is_yours" in response_marker["properties"]
            and response_marker["properties"]["is_yours"] is False
        ), "is_yours can't be true in unauthorized marker instance response"

        assert (
            "is_yours" in response_owner_story
            and response_owner_story["is_yours"] is False
        ), "is_yours for story can't be true in unauthorized marker instance response"

    @pytest.mark.django_db()
    def test_marker_instance_authorized(
        self,
        user_owner_client,
        marker_with_author_story,
        second_story_for_marker_author_user,
        user_owner_instance,
        simple_story_data,
    ):
        """Tests unauthorized request to marker instance.
        Checks that in response is_yours for marker is true.
        Checks that in response is_yours for owner story is true.
        Checks that in response is_yours for other user story is false."""

        response_marker, response_owner_story = self.check_marker_instance(
            user_owner_client,
            marker_with_author_story,
            user_owner_instance,
            simple_story_data,
        )
        assert (
            "is_yours" in response_marker["properties"]
            and response_marker["properties"]["is_yours"] is True
        ), "is_yours must be true in authorized marker response for this marker"

        assert (
            "is_yours" in response_owner_story
            and response_owner_story["is_yours"] is True
        ), "is_yours for story with author owner must be true it authorised response"

        # is_yours for other user story
        response_other_user_story = next(
            (
                story
                for story in response_marker["properties"]["stories"]
                if story["id"] == second_story_for_marker_author_user.id
            ),
            None,
        )
        assert (
            response_other_user_story
        ), "No orher user story in marker instance response"
        assert (
            "is_yours" in response_owner_story
            and response_other_user_story["is_yours"] is False
        ), "is_yours for other user story must be false in marker instance response"

    # TODO: PATCH
    # TODO: DELETE
    # TODO: PUT
