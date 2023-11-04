import pytest

from .common import check_response


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

    # CREATE
    @pytest.mark.django_db()
    def test_marker_create_unauthorized(self, client, simple_marker_json):
        response = client.post(self.URL_MARKERS, data=simple_marker_json, format="json")
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "blank_field",
        ["name", "location"],
    )
    def test_marker_create_blank_field(
        self,
        user_owner_client,
        simple_marker_json,
        blank_field,
    ):
        simple_marker_json[blank_field] = None
        response = user_owner_client.post(
            self.URL_MARKERS, data=simple_marker_json, format="json"
        )
        check_response(response, 400, [blank_field])

    @pytest.mark.django_db()
    def test_marker_create_location_exist(
        self,
        user_owner_client,
        simple_marker,
        simple_marker_json,
    ):
        response = user_owner_client.post(
            self.URL_MARKERS,
            data=simple_marker_json,
            format="json",
        )
        check_response(response, 400, ["coordinates"])

    @pytest.mark.django_db()
    def test_marker_create_valid(self, user_owner_client, simple_marker_json):
        response = user_owner_client.post(
            self.URL_MARKERS, data=simple_marker_json, format="json"
        )

        required_fields = [
            "id",
            "type",
            "geometry",
            "properties",
        ]
        check_response(response, 201, required_fields)
        assert (
            "name" in response.data["properties"]
            and response.data["properties"]["name"] == simple_marker_json["name"]
        ), "Name in response data doesn't match json name"
        assert (
            "is_yours" in response.data["properties"]
            and response.data["properties"]["is_yours"] is True
        ), "is_yours must be true for tour marker"
        assert (
            "type" in response.data["geometry"]
            and response.data["geometry"]["type"] == "Point"
        ), "Wrong geometry type in response"
        assert (
            "coordinates" in response.data["geometry"]
            and response.data["geometry"]["coordinates"]
            == simple_marker_json["location"]["coordinates"]
        ), "Geometry location in response doest't match jsons coordinates"
        assert (
            "stories" not in response.data
        ), "Response shusn't include stories for new marker"

    # PATCH
    @pytest.mark.django_db()
    def test_marker_patch_unauthorized(
        self, client, simple_marker, simple_marker_updated_json
    ):
        url = f"{self.URL_MARKERS}{simple_marker.id}/"
        response = client.patch(url, data=simple_marker_updated_json, format="json")
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    @pytest.mark.parametrize(
        "blank_field",
        ["name", "location"],
    )
    def test_marker_patch_blank_field(
        self,
        user_owner_client,
        marker_with_author_story,
        simple_marker_updated_json,
        blank_field,
    ):
        url = f"{self.URL_MARKERS}{marker_with_author_story.id}/"
        simple_marker_updated_json[blank_field] = None
        response = user_owner_client.patch(
            url, data=simple_marker_updated_json, format="json"
        )
        check_response(response, 400, [blank_field])

    @pytest.mark.django_db()
    def test_marker_patch_location_exist(
        self,
        user_owner_client,
        simple_marker,
        marker_with_author_story,
        simple_marker_updated_json_same_location,
    ):
        url = f"{self.URL_MARKERS}{marker_with_author_story.id}/"
        response = user_owner_client.patch(
            url, data=simple_marker_updated_json_same_location, format="json"
        )
        check_response(response, 400, ["coordinates"])

    @pytest.mark.django_db()
    def test_marker_patch_valid_new_name(
        self, user_owner_client, marker_with_author_story, simple_marker_updated_json
    ):
        url = f"{self.URL_MARKERS}{marker_with_author_story.id}/"
        response = user_owner_client.patch(
            url, data={"name": simple_marker_updated_json["name"]}
        )

        required_fields = [
            "id",
            "type",
            "geometry",
            "properties",
        ]
        check_response(response, 200, required_fields)
        assert (
            response.data["properties"]["name"] == simple_marker_updated_json["name"]
        ), "Name in response data doesn't match patched name"

    @pytest.mark.django_db()
    def test_marker_patch_valid_new_location(
        self, user_owner_client, marker_with_author_story, simple_marker_updated_json
    ):
        url = f"{self.URL_MARKERS}{marker_with_author_story.id}/"
        response = user_owner_client.patch(
            url,
            data={"location": simple_marker_updated_json["location"]},
            format="json",
        )

        required_fields = [
            "id",
            "type",
            "geometry",
            "properties",
        ]
        check_response(response, 200, required_fields)
        assert (
            "type" in response.data["geometry"]
            and "coordinates" in response.data["geometry"]
        ), "Wrong response location format"

        assert (
            response.data["geometry"]["coordinates"]
            == simple_marker_updated_json["location"]["coordinates"]
        ), "Updated coordinates in response data doesn't match patched location"

    # TODO: DELETE
    @pytest.mark.django_db()
    def test_marker_delete_unauthorized(self, client, simple_marker):
        url = f"{self.URL_MARKERS}{simple_marker.id}/"
        response = client.delete(url)
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_marker_delete_not_owner(self, user_client, marker_with_author_story):
        url = f"{self.URL_MARKERS}{marker_with_author_story.id}/"
        response = user_client.delete(url)

        check_response(response, 403, ["detail"])

    @pytest.mark.django_db()
    def test_marker_delete_empty_owner(self, user_owner_client, simple_marker):
        url = f"{self.URL_MARKERS}{simple_marker.id}/"
        response = user_owner_client.delete(url)

        check_response(response, 403, ["detail"])

    @pytest.mark.django_db()
    def test_marker_delete_owner(self, user_owner_client, marker_with_author_story):
        url = f"{self.URL_MARKERS}{marker_with_author_story.id}/"
        response = user_owner_client.delete(url)

        check_response(response, 204)

    # TODO: PUT
    @pytest.mark.django_db()
    def test_marker_put_unauthorized(
        self, client, simple_marker, simple_marker_updated_json
    ):
        url = f"{self.URL_MARKERS}{simple_marker.id}/"
        response = client.put(url, data=simple_marker_updated_json, format="json")
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_marker_put_owner(
        self, user_owner_client, marker_with_author_story, simple_marker_updated_json
    ):
        url = f"{self.URL_MARKERS}{marker_with_author_story.id}/"
        response = user_owner_client.put(
            url, data=simple_marker_updated_json, format="json"
        )

        check_response(response, 403, ["detail"])
