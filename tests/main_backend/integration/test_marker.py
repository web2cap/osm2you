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
        assert "geometry" in response_simple_marker, (
            "No geometry in marker list response"
        )
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
        assert "properties" in response_simple_marker, (
            "No properties in marker list response"
        )
        assert (
            "name" in response_simple_marker["properties"]
            and response_simple_marker["properties"]["name"] == marker.name
        ), "Wrong name in marker list response"

        return response_simple_marker

    @pytest.mark.skip("Todo markers with clustering tests")
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

    @pytest.mark.skip("Todo markers with clustering tests")
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
        assert "add_date" in response.data["properties"] and response.data[
            "properties"
        ]["add_date"] == marker.add_date.strftime("%Y-%m-%dT%H:%M:%S.%f"), (
            "Wrong add_date in marker response"
        )

        # Storise in marker
        assert "stories" in response.data["properties"], "No stories in marker response"
        assert len(response.data["properties"]["stories"]) == 2, (
            "Stories in marker response must include 2 story"
        )
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
        assert "id" in response_owner_story and response_owner_story["id"], (
            "Wrong story id field"
        )
        assert "text" in response_owner_story and simple_story_data["text"], (
            "Wrong story text field"
        )
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
        Checks that in response is_yours for story is false."""

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
        assert response_other_user_story, (
            "No orher user story in marker instance response"
        )
        assert (
            "is_yours" in response_owner_story
            and response_other_user_story["is_yours"] is False
        ), "is_yours for other user story must be false in marker instance response"

    @pytest.mark.django_db()
    def test_marker_instance_tags(
        self,
        client,
        marker_with_tag,
    ):
        """Tests tags in unauthorized request to marker instance."""

        response_marker = client.get(f"{self.URL_MARKERS}{marker_with_tag.id}/")
        required_fields = ["id", "type", "geometry", "properties"]
        check_response(response_marker, 200, required_fields)
        response_json = response_marker.json()

        assert "tags" in response_json["properties"], (
            "Field tags should be present in valid response."
        )

        assert len(response_json["properties"]["tags"]), (
            "Field tags  should content elemet."
        )

        isinstance_tag_value = marker_with_tag.tag_value.first()

        assert isinstance_tag_value.tag.name in response_json["properties"]["tags"], (
            "Field with tag name should be present in valid response."
        )

        assert (
            response_json["properties"]["tags"][isinstance_tag_value.tag.name]
            == isinstance_tag_value.value
        ), "Field with tag value should be equal instance tag value."

    # CREATE
    @pytest.mark.django_db()
    def test_marker_create_unauthorized(self, client, simple_marker_json):
        response = client.post(self.URL_MARKERS, data=simple_marker_json, format="json")
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_marker_create_blank_field(
        self,
        user_owner_client,
        simple_marker_json,
    ):
        simple_marker_json["location"] = None
        response = user_owner_client.post(
            self.URL_MARKERS, data=simple_marker_json, format="json"
        )
        check_response(response, 400, ["location"])

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
        check_response(response, 400, ["location"])

    @pytest.mark.django_db()
    def test_marker_create_valid_no_name(
        self, user_owner_client, simple_marker_json, main_kind
    ):
        simple_marker_json.pop("name")
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
            and response.data["properties"]["name"] is None
        ), "Name in response data doesn't equal None"

    @pytest.mark.django_db()
    def test_marker_create_valid(
        self, user_owner_client, simple_marker_json, main_kind
    ):
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
        ), "is_yours must be true for your marker"
        assert (
            "type" in response.data["geometry"]
            and response.data["geometry"]["type"] == "Point"
        ), "Wrong geometry type in response"
        assert (
            "coordinates" in response.data["geometry"]
            and response.data["geometry"]["coordinates"]
            == simple_marker_json["location"]["coordinates"]
        ), "Geometry location in response doest't match jsons coordinates"
        assert "stories" not in response.data, (
            "Response shusn't include stories for new marker"
        )

    # PATCH
    @pytest.mark.django_db()
    def test_marker_patch_unauthorized(
        self, client, simple_marker, simple_marker_updated_json
    ):
        url = f"{self.URL_MARKERS}{simple_marker.id}/"
        response = client.patch(url, data=simple_marker_updated_json, format="json")
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_marker_patch_blank_field(
        self,
        user_owner_client,
        camp_site_marker_with_author_story,
        simple_marker_updated_json,
    ):
        url = f"{self.URL_MARKERS}{camp_site_marker_with_author_story.id}/"
        simple_marker_updated_json["location"] = None
        response = user_owner_client.patch(
            url, data=simple_marker_updated_json, format="json"
        )
        check_response(response, 400, ["location"])

    @pytest.mark.django_db()
    def test_marker_patch_location_exist(
        self,
        user_owner_client,
        simple_marker,
        camp_site_marker_with_author_story,
        simple_marker_updated_json_same_location,
    ):
        url = f"{self.URL_MARKERS}{camp_site_marker_with_author_story.id}/"
        response = user_owner_client.patch(
            url, data=simple_marker_updated_json_same_location, format="json"
        )
        check_response(response, 400, ["location"])

    @pytest.mark.django_db()
    def test_marker_patch_valid_new_name(
        self,
        user_owner_client,
        camp_site_marker_with_author_story,
        simple_marker_updated_json,
    ):
        url = f"{self.URL_MARKERS}{camp_site_marker_with_author_story.id}/"
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
        self,
        user_owner_client,
        camp_site_marker_with_author_story,
        simple_marker_updated_json,
    ):
        url = f"{self.URL_MARKERS}{camp_site_marker_with_author_story.id}/"
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

    # DELETE
    @pytest.mark.django_db()
    def test_marker_delete_unauthorized(self, client, simple_marker):
        url = f"{self.URL_MARKERS}{simple_marker.id}/"
        response = client.delete(url)
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_marker_delete_not_owner(
        self, user_client, camp_site_marker_with_author_story
    ):
        url = f"{self.URL_MARKERS}{camp_site_marker_with_author_story.id}/"
        response = user_client.delete(url)

        check_response(response, 403, ["detail"])

    @pytest.mark.django_db()
    def test_marker_delete_empty_owner(
        self, user_owner_client, camp_site_marker_with_author_story
    ):
        camp_site_marker_with_author_story.author = None
        camp_site_marker_with_author_story.save()
        url = f"{self.URL_MARKERS}{camp_site_marker_with_author_story.id}/"
        response = user_owner_client.delete(url)

        check_response(response, 403, ["detail"])

    @pytest.mark.django_db()
    def test_marker_delete_owner(
        self, user_owner_client, camp_site_marker_with_author_story
    ):
        url = f"{self.URL_MARKERS}{camp_site_marker_with_author_story.id}/"
        response = user_owner_client.delete(url)

        check_response(response, 204)

    # PUT
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

    # ACTION USER
    def check_marker_author_list(self, client, marker, username, markers_count):
        """Tests a request to markers list.
        Checks the number of markers in the list.
        Checking the fields and field values of one marker in the list.
        Returns the response element of a single marker for detailed checking."""

        response = client.get(f"{self.URL_MARKERS}user/{username}/")
        required_fields = ["type", "features"]
        check_response(response, 200, required_fields)

        assert len(response.data["features"]) == markers_count, (
            f"Response must has {markers_count} markers"
        )

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
        assert "geometry" in response_simple_marker, (
            "No geometry in marker list response"
        )
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
        assert "properties" in response_simple_marker, (
            "No properties in marker list response"
        )
        assert (
            "name" in response_simple_marker["properties"]
            and response_simple_marker["properties"]["name"] == marker.name
        ), "Wrong name in marker list response"

        return response_simple_marker

    @pytest.mark.django_db()
    def test_marker_user_action_unauthorized(
        self, client, simple_marker, marker_with_author_story
    ):
        """Tests unauthorized request to marker user action.
        Chech that marker include story with text."""

        response_simple_marker = self.check_marker_author_list(
            client,
            marker_with_author_story,
            marker_with_author_story.author.username,
            markers_count=1,
        )
        assert "stories" in response_simple_marker["properties"], (
            "No stories field in response"
        )
        assert len(response_simple_marker["properties"]["stories"]), (
            "No  one story in response"
        )
        assert "text" in response_simple_marker["properties"]["stories"][0], (
            "No text field of story in response"
        )
        assert (
            response_simple_marker["properties"]["stories"][0]["text"]
            == marker_with_author_story.stories.first().text
        ), "Response story text doesn't eqal story instance text"

    @pytest.mark.django_db()
    def test_marker_user_action_authorized(
        self, client, simple_marker, marker_with_author_story
    ):
        """Tests authorized request to marker user action.
        Chech that marker include story with text."""

        response_simple_marker = self.check_marker_author_list(
            client,
            marker_with_author_story,
            marker_with_author_story.author.username,
            markers_count=1,
        )
        assert "stories" in response_simple_marker["properties"], (
            "No stories field in response"
        )
        assert len(response_simple_marker["properties"]["stories"]), (
            "No  one story in response"
        )
        assert "text" in response_simple_marker["properties"]["stories"][0], (
            "No text field of story in response"
        )
        assert (
            response_simple_marker["properties"]["stories"][0]["text"]
            == marker_with_author_story.stories.first().text
        ), "Response story text doesn't eqal story instance text"

    @pytest.mark.django_db()
    def test_marker_user_action_dataset(
        self,
        client,
        simple_marker,
        marker_with_author_story,
        marker_different_author_with_story_owner_story_user,
        simple_story_data,
    ):
        """Test that response include 2 expected markers from 3.
        One with users marker, other with marker with users story.
        Test that response include onlu users stories."""

        self.check_marker_author_list(
            client,
            marker_with_author_story,
            marker_with_author_story.author.username,
            markers_count=2,
        )
        response_different_author = self.check_marker_author_list(
            client,
            marker_different_author_with_story_owner_story_user,
            marker_with_author_story.author.username,
            markers_count=2,
        )

        assert "stories" in response_different_author["properties"], (
            "No stories field in response"
        )
        assert len(response_different_author["properties"]["stories"]) == 1, (
            "Expected 1 story in this marker response"
        )
        assert (
            "text" in response_different_author["properties"]["stories"][0]
            and response_different_author["properties"]["stories"][0]["text"]
            == simple_story_data["text"]
        ), "Response story text doesn't eqal simple_story_data text"
