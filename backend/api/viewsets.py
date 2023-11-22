from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from markers.models import Marker
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_gis import filters
from stories.models import Story
from users.models import User

from .permissions import AuthorAdminOrInstanceOnly, AuthorAdminOrReadOnly
from .serializers import (
    MarkerInstanceSerializer,
    MarkerSerializer,
    MarkerUserSerializer,
    StorySerializer,
    StorySerializerDisplay,
    StorySerializerText,
)


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker view set."""

    permission_classes = (AuthorAdminOrReadOnly,)

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)

    serializers = {
        "retrieve": MarkerInstanceSerializer,
        "user": MarkerUserSerializer,
        "default": MarkerSerializer,
    }

    def get_serializer_class(self):
        """Get the serializer class based on the action."""
        return self.serializers.get(self.action, self.serializers["default"])

    def get_queryset(self):
        """Get the queryset for Marker objects.
        If retrive join author ans stories to marker and author to story.
        """
        queryset = Marker.objects.all()
        if self.action in ("retrieve"):
            queryset = Marker.objects.select_related("author").prefetch_related(
                Prefetch(
                    "stories",
                    queryset=Story.objects.select_related("author"),
                ),
                "stories__author",
            )
        return queryset

    def get_user_markers_queryset(self, user):
        """Select users markers and markers with users stories."""

        return Marker.objects.filter(
            Q(stories__isnull=False, stories__author=user) | Q(author=user)
        ).prefetch_related(
            Prefetch(
                "stories",
                queryset=Story.objects.filter(author=user),
            )
        )

    def perform_create(self, serializer):
        """Add autorized user to author field."""

        serializer.save(author=self.request.user)

    @action(methods=["get"], detail=False, url_path="user/(?P<username>[^/.]+)")
    def user(self, request, username):
        """Markers with users stories and users markers by users username."""

        user = get_object_or_404(User, username=username)
        queryset = self.get_user_markers_queryset(user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StoryViewSet(viewsets.ModelViewSet):
    """Story view set."""

    queryset = Story.objects.select_related("author").all()
    permission_classes = (AuthorAdminOrInstanceOnly,)
    serializers = {
        "list": StorySerializerDisplay,
        "retrieve": StorySerializerDisplay,
        "partial_update": StorySerializerText,
        "default": StorySerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers["default"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
