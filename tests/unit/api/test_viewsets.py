import pytest
from api.serializers import (
    MarkerInstanceSerializer,
    MarkerSerializer,
    MarkerUserSerializer,
)
from markers.models import Marker


class TestMarkerViewset:
    """Tests marker viewset."""

    @pytest.mark.django_db
    def test_get_serializer_class(
        self,
        marker_viewset_instance_list,
        marker_viewset_instance_retrieve,
        marker_viewset_instance_user,
    ):
        """Test that for list action viewset use MarkerSerializer.
        For action retrieve viewset use MarkerInstanceSerializer.
        For action user viewset use MarkerUserSerializer."""

        assert (
            marker_viewset_instance_list.get_serializer_class() == MarkerSerializer
        ), "For list action viewset should use MarkerSerializer"
        assert (
            marker_viewset_instance_retrieve.get_serializer_class()
            == MarkerInstanceSerializer
        ), "For retrieve action viewset should use MarkerInstanceSerializer"
        assert (
            marker_viewset_instance_user.get_serializer_class() == MarkerUserSerializer
        ), "For user action viewset should use MarkerUserSerializer"

    @pytest.mark.django_db
    def test_get_queryset_retrieve(
        self,
        marker_viewset_instance_retrieve,
        marker_with_author_story,
        user_owner_instance,
        simple_story_data,
    ):
        """Test are marker, marker author, stories, stories author present in queryset.
        If action is retrieve."""
        queryset = marker_viewset_instance_retrieve.get_queryset()
        assert (
            marker_with_author_story in queryset
        ), "No marker in marker retrieve queryset"
        assert (
            queryset.first().author == user_owner_instance
        ), "No marker author in marker retrieve queryset"
        assert (
            queryset.first().stories.first().text == simple_story_data["text"]
        ), "No story in marker retrieve queryset"
        assert (
            queryset.first().stories.first().author == user_owner_instance
        ), "No stories author marker in retrieve queryset"

    @pytest.mark.django_db
    def test_get_queryset_list(
        self,
        marker_viewset_instance_list,
        marker_with_author_story,
        user_owner_instance,
    ):
        """Test are marker, marker author present in list queryset."""
        queryset = marker_viewset_instance_list.get_queryset()
        assert marker_with_author_story in queryset, "No marker in marker list queryset"
        assert (
            queryset.first().author == user_owner_instance
        ), "No marker author in marker list queryset"

    @pytest.mark.django_db
    def test_perform_create(self, marker_viewset, owner_request, simple_marker_data):
        """Test marker perform create, that add author from request.user."""
        marker_viewset.request = owner_request
        marker_serializer = MarkerSerializer(data=simple_marker_data)
        if marker_serializer.is_valid():
            marker_viewset.perform_create(marker_serializer)
        new_marker = Marker.objects.get(name=simple_marker_data["name"])
        assert new_marker.author == owner_request.user

    @pytest.mark.django_db
    def test_perform_create_mock(self, marker_viewset, simple_marker_data):
        """Test marker perform create, that raise error if request.user is empty."""
        marker_viewset.request = None
        marker_serializer = MarkerSerializer(data=simple_marker_data)
        with pytest.raises(AttributeError):
            marker_serializer.is_valid()
            marker_viewset.perform_create(marker_serializer)

    @pytest.mark.django_db
    def test_get_user_markers_queryset(
        self, marker_viewset_instance_user, marker_with_author_story
    ):
        user = marker_with_author_story.author
        queryset = marker_viewset_instance_user.get_user_markers_queryset(user)

        assert marker_with_author_story in queryset, "No marker in markers queryset"
        assert (
            marker_with_author_story.stories.first() in queryset.first().stories.all()
        ), "No story in markers queryset"


class TestStoryViewset:
    """Tests marker viewset."""

    @pytest.mark.django_db
    def test_get_queryset(
        self, story_viewset, simple_story, user_owner_instance, simple_marker
    ):
        """Test are story, marker, author in story queryset."""
        queryset = story_viewset.get_queryset()
        assert simple_story in queryset, "No story in story queryset"
        assert (
            queryset.first().author == user_owner_instance
        ), "No story author in story queryset"
        assert (
            queryset.first().marker == simple_marker
        ), "No story marker in story queryset"
