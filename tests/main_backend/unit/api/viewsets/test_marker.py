import pytest
from api.serializers.markers import (
    MarkerClusterSerializer,
    MarkerInstanceSerializer,
    MarkerSerializer,
    MarkerUserSerializer,
)
from core.models.markers import Marker


class TestMarkerViewset:
    """Tests marker viewset."""

    @pytest.mark.django_db
    def test_get_serializer_class(
        self,
        marker_viewset_instance_list_large_zoom,
        marker_viewset_instance_list_small_zoom,
        marker_viewset_instance_retrieve,
        marker_viewset_instance_user,
    ):
        """Test that for list action viewset and large zoom use MarkerClusterSerializer.
        For list action viewset and small zoom use MarkerSerializer.
        For action retrieve viewset use MarkerInstanceSerializer.
        For action user viewset use MarkerUserSerializer."""

        assert (
            marker_viewset_instance_list_large_zoom.get_serializer_class()
            == MarkerSerializer
        ), "For list action viewset with large zoom should use MarkerSerializer"
        assert (
            marker_viewset_instance_retrieve.get_serializer_class()
            == MarkerInstanceSerializer
        ), "For retrieve action viewset should use MarkerInstanceSerializer"
        assert (
            marker_viewset_instance_user.get_serializer_class() == MarkerUserSerializer
        ), "For user action viewset should use MarkerUserSerializer"

        assert (
            marker_viewset_instance_list_small_zoom.get_serializer_class()
            == MarkerClusterSerializer
        ), "For list action with small zoom viewset should use MarkerClusterSerializer"

    @pytest.mark.django_db
    def test_get_queryset_retrieve(
        self,
        marker_viewset_instance_retrieve,
        marker_with_author_story,
        user_owner_instance,
        simple_story_data,
        simple_tagǜalue_withoutmarker_data,
    ):
        """Test are marker, marker author, stories, stories author present in queryset.
        If action is retrieve."""
        queryset = marker_viewset_instance_retrieve.get_queryset()
        assert marker_with_author_story in queryset, (
            "No marker in marker retrieve queryset"
        )
        assert queryset.first().author == user_owner_instance, (
            "No marker author in marker retrieve queryset"
        )
        assert queryset.first().stories.first().text == simple_story_data["text"], (
            "No story in marker retrieve queryset"
        )
        assert queryset.first().stories.first().author == user_owner_instance, (
            "No stories author marker in retrieve queryset"
        )
        marker_with_author_story.tag_value.create(**simple_tagǜalue_withoutmarker_data)
        assert (
            queryset.first().tag_value.first().tag
            == simple_tagǜalue_withoutmarker_data["tag"]
        )
        assert (
            queryset.first().tag_value.first().value
            == simple_tagǜalue_withoutmarker_data["value"]
        )

    @pytest.mark.django_db
    def test_perform_create(
        self, marker_viewset, owner_request, simple_marker_data, main_kind
    ):
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
