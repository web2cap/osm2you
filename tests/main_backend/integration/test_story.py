import pytest

from .common import check_response


class TestStory:
    URL_STORIES = "/api/v1/stories/"

    # GET INSTANCE

    def check_story_instance(self, client, story):
        """Tests a request to story instance.
        Checking the fields and field values of story in the list.
        Returns the response data of a story for detailed checking.
        """

        response = client.get(f"{self.URL_STORIES}{story.id}/")
        required_fields = [
            "id",
            "text",
            "author",
        ]

        check_response(response, 200, required_fields)

        assert response.data["id"] == story.id, (
            "Wrong story id in story instance respone"
        )
        assert response.data["text"] == story.text, (
            "Wrong story text in story instance respone"
        )

        assert (
            "first_name" in response.data["author"]
            and response.data["author"]["first_name"] == story.author.first_name
        ), "Wrong author first_name in story instance respone"
        assert (
            "username" in response.data["author"]
            and response.data["author"]["username"] == story.author.username
        ), "Wrong author username in story instance respone"

        return response.data

    @pytest.mark.django_db()
    def test_story_instance_unauthorized(
        self,
        client,
        simple_story,
    ):
        """Tests unauthorized request to story instance.
        Checks that in response is_yours for story is false."""

        response_story = self.check_story_instance(client, simple_story)

        assert "is_yours" in response_story and response_story["is_yours"] is False, (
            "is_yours can't be true in unauthorized story instance response"
        )

    @pytest.mark.django_db()
    def test_story_instance_authorized_owner(
        self,
        user_owner_client,
        simple_story,
    ):
        """Tests authorized request from owner to story instance.
        Checks that in response is_yours for story is true."""

        response_story = self.check_story_instance(user_owner_client, simple_story)

        assert "is_yours" in response_story and response_story["is_yours"] is True, (
            "is_yours must be true in owner story instance response"
        )

    @pytest.mark.django_db()
    def test_story_instance_authorized_other_user(
        self,
        user_client,
        simple_story,
    ):
        """Tests autorised request from other user to story instance.
        Checks that in response is_yours for story is false."""

        response_story = self.check_story_instance(user_client, simple_story)

        assert "is_yours" in response_story and response_story["is_yours"] is False, (
            "is_yours must be false in other user story instance response"
        )

    # CREATE
    @pytest.mark.django_db()
    def test_story_create_unauthorized(self, client, simple_story_json):
        response = client.post(self.URL_STORIES, data=simple_story_json, format="json")
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_story_create_blank_text(
        self,
        user_owner_client,
        simple_story_json,
    ):
        simple_story_json["text"] = None
        response = user_owner_client.post(
            self.URL_STORIES, data=simple_story_json, format="json"
        )
        check_response(response, 400, ["text"])

    @pytest.mark.django_db()
    def test_story_create_valid(
        self, user_owner_client, simple_story_json, user_owner_instance
    ):
        response = user_owner_client.post(
            self.URL_STORIES, data=simple_story_json, format="json"
        )

        required_fields = ["id", "text", "author", "marker"]
        check_response(response, 201, required_fields)
        assert response.data["text"] == simple_story_json["text"], (
            "Text in response data doesn't match json text"
        )

        assert response.data["author"] == user_owner_instance.id, (
            "Wrong author id in story instance response"
        )

    @pytest.mark.django_db()
    def test_story_create_short_text(
        self, user_owner_client, simple_story_json, user_owner_instance
    ):
        simple_story_json["text"] = simple_story_json["text"][:8]
        response = user_owner_client.post(
            self.URL_STORIES, data=simple_story_json, format="json"
        )

        check_response(response, 400, ["text"])

    # PATCH
    @pytest.mark.django_db()
    def test_story_patch_unauthorized(self, client, simple_story, simple_story_json):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = client.patch(url, data=simple_story_json, format="json")
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_story_patch_blank_text(
        self,
        user_owner_client,
        simple_story,
    ):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = user_owner_client.patch(url, data={"text": None}, format="json")
        check_response(response, 400, ["text"])

    @pytest.mark.django_db()
    def test_story_patch_short_text(
        self,
        user_owner_client,
        simple_story,
    ):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        short_text = simple_story.text[:8]
        response = user_owner_client.patch(
            url, data={"text": short_text}, format="json"
        )
        check_response(response, 400, ["text"])

    @pytest.mark.django_db()
    def test_story_patch_other_marker(
        self,
        user_owner_client,
        simple_story,
        simple_marker,
        marker_with_author_story,
    ):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = user_owner_client.patch(
            url, data={"marker": marker_with_author_story}
        )
        check_response(response, 200, ["text"])
        assert simple_story.marker == simple_marker, "Story marker isn't patchable."

    @pytest.mark.django_db()
    def test_story_patch_other_user(
        self, user_client, simple_story, simple_story_update_json
    ):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = user_client.patch(url, data=simple_story_update_json, format="json")

        required_fields = ["detail"]
        check_response(response, 403, required_fields)

    @pytest.mark.django_db()
    def test_story_patch_valid(
        self, user_owner_client, simple_story, simple_story_update_json
    ):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = user_owner_client.patch(
            url, data=simple_story_update_json, format="json"
        )

        required_fields = ["text"]
        check_response(response, 200, required_fields)

    # DELETE
    @pytest.mark.django_db()
    def test_story_delete_unauthorized(self, client, simple_story):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = client.delete(url)
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_story_delete_not_owner(self, user_client, simple_story):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = user_client.delete(url)
        check_response(response, 403, ["detail"])

    @pytest.mark.django_db()
    def test_story_delete_owner(self, user_owner_client, simple_story):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = user_owner_client.delete(url)
        check_response(response, 204)

    # PUT
    @pytest.mark.django_db()
    def test_story_put_unauthorized(self, client, simple_story, simple_story_json):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = client.put(url, data=simple_story_json, format="json")
        check_response(response, 401, ["detail"])

    @pytest.mark.django_db()
    def test_story_put_owner(self, user_owner_client, simple_story, simple_story_json):
        url = f"{self.URL_STORIES}{simple_story.id}/"
        response = user_owner_client.put(url, data=simple_story_json, format="json")

        check_response(response, 403, ["detail"])
