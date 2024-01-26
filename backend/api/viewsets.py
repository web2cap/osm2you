from django.conf import settings

# from django.contrib.gis.geos import Point
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from markers.models import Marker, MarkerCluster
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_gis import filters
from stories.models import Story
from tags.models import TagValue
from users.models import User

from .permissions import AuthorAdminOrInstanceOnly, AuthorAdminOrReadOnly
from .serializers import (
    CustomUserInfoSerializer,
    MarkerClusterSerializer,
    MarkerInstanceSerializer,
    MarkerSerializer,
    MarkerUserSerializer,
    StorySerializer,
    StorySerializerDisplay,
    StorySerializerText,
)

CLUSTERING = getattr(settings, "CLUSTERING", {})
CLUSTERING_DENCITY = getattr(settings, "CLUSTERING_DENCITY", 36)


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker view set."""

    permission_classes = (AuthorAdminOrReadOnly,)

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)

    serializers = {
        "retrieve": MarkerInstanceSerializer,
        "user": MarkerUserSerializer,
        "clusters": MarkerClusterSerializer,
        "default": MarkerSerializer,
    }

    def get_serializer_class(self):
        """Get the serializer class based on the action."""

        if self.action == "list" and self.zoom_level():
            return self.serializers.get("clusters")
        return self.serializers.get(self.action, self.serializers["default"])

    def get_queryset(self):
        """Gets the queryset for Marker objects.
        If action is retrieve, joins author and stories with story author to marker.
        If action is retrieve, joins tags values and this tags names to marker.
        """

        zoom_level = self.zoom_level()
        queryset = Marker.objects.all()
        if self.action == "retrieve":
            queryset = Marker.objects.select_related("author").prefetch_related(
                Prefetch(
                    "stories",
                    queryset=Story.objects.select_related("author"),
                ),
                "stories__author",
                Prefetch(
                    "tag_value",
                    queryset=TagValue.objects.select_related("tag"),
                ),
                "tag_value__tag",
            )
        elif self.action == "list" and zoom_level:
            queryset = MarkerCluster.objects.all()
        return queryset

    def get_user_markers_queryset(self, user):
        """Select users markers and markers with users stories."""

        return (
            Marker.objects.filter(
                Q(stories__isnull=False, stories__author=user) | Q(author=user)
            )
            .distinct()
            .prefetch_related(
                Prefetch(
                    "stories",
                    queryset=Story.objects.filter(author=user),
                )
            )
        )

    def perform_create(self, serializer):
        """Add autorized user to author field."""

        serializer.save(author=self.request.user)

    @action(methods=["get"], detail=False, url_path="user/(?P<username>[^/.]+)")
    def user(self, request, username):
        """Chech if usernmame exists get user. Add user info to response.
        Add markers with users stories and users markers."""

        user = get_object_or_404(User, username=username)
        user_data = {"user": CustomUserInfoSerializer(user).data}

        markers_queryset = self.filter_queryset(self.get_user_markers_queryset(user))
        markers_data = self.get_serializer(markers_queryset, many=True).data

        return Response(user_data | markers_data)

    def get_bbox_area(self):
        bbox = self.request.query_params.get("in_bbox")
        if not bbox:
            return 360 * 180

        min_lon, min_lat, max_lon, max_lat = map(float, bbox.split(","))
        dif_lon = max_lon - min_lon
        if dif_lon > 360:
            dif_lon = 360
        dif_lat = max_lat - min_lat
        if dif_lat > 180:
            dif_lon = 180
        return dif_lon * dif_lat

    def zoom_level(self):
        """Calculate the zoom level based on CLUSTERING_DENCITY and bbox area."""
        bbox_area = self.get_bbox_area()
        if bbox_area < CLUSTERING["square_size"][0] ** 2 * CLUSTERING_DENCITY:
            return False

        for i in range(1, len(CLUSTERING["square_size"])):
            if bbox_area < CLUSTERING["square_size"][i] ** 2 * CLUSTERING_DENCITY:
                return CLUSTERING["zoom"][i - 1]

        return CLUSTERING["zoom"][len(CLUSTERING["square_size"]) - 1]


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
