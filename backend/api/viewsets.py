from django.conf import settings
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from markers.models import Marker, MarkerCluster
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_gis import filters
from stories.models import Story
from tags.models import Tag, TagValue
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
MARKERS_KIND_MAIN = getattr(settings, "MARKERS_KIND_MAIN")


class MarkerViewSet(viewsets.ModelViewSet):
    """ViewSet for handling Marker objects, including clustering logic."""

    permission_classes = (AuthorAdminOrReadOnly,)
    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)

    serializers = {
        "retrieve": MarkerInstanceSerializer,
        "user": MarkerUserSerializer,
        "clusters": MarkerClusterSerializer,
        "default": MarkerSerializer,
    }

    calculated_square_size = None

    def get_serializer_class(self):
        """Get the appropriate serializer class based on the action."""

        if self.action == "list" and self.square_size():
            return self.serializers.get("clusters")
        return self.serializers.get(self.action, self.serializers["default"])

    def get_queryset(self):
        """Get the queryset for Marker objects or MarkerCluster objects based on the action.
        List only markers with MARKERS_KIND_MAIN tag present."""
        if self.action == "retrieve":
            return self.get_retrieve_queryset()
        if self.action == "list" and self.square_size():
            return self.get_cluster_queryset()

        main_kind_tag = get_object_or_404(Tag, name=MARKERS_KIND_MAIN["tag"])
        return Marker.objects.filter(
            tag_value__tag=main_kind_tag,
            tag_value__value=MARKERS_KIND_MAIN["tag_value"],
        )

    def get_retrieve_queryset(self):
        """Get the queryset for Marker objects with additional related data for the 'retrieve' action."""

        return Marker.objects.select_related("author").prefetch_related(
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

    def get_cluster_queryset(self):
        """Get the queryset for MarkerCluster objects based on the current square size."""

        return MarkerCluster.objects.filter(square_size=self.square_size())

    def get_user_markers_queryset(self, user):
        """Get the queryset for markers associated with a specific user and their stories."""

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
        """Add the authorized user to the author field during marker creation."""

        serializer.save(author=self.request.user)

    @action(methods=["get"], detail=False, url_path="user/(?P<username>[^/.]+)")
    def user(self, request, username):
        """Check if a username exists, get the user, and add user info to the response.
        Add markers with users stories and users markers."""

        user = get_object_or_404(User, username=username)
        user_data = {"user": CustomUserInfoSerializer(user).data}

        markers_queryset = self.filter_queryset(self.get_user_markers_queryset(user))
        markers_data = self.get_serializer(markers_queryset, many=True).data

        return Response(user_data | markers_data)

    def get_bbox_area(self):
        """Calculate and return the area of the bounding box specified in the request parameters.

        Returns:
            float: The area of the bounding box.
        """

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

    def square_size(self):
        """Calculate and return the square_size level based on CLUSTERING_DENCITY and bounding box area.

        Returns:
            int or False: The calculated square_size level, or False if the zoom is too large.
        """
        if self.calculated_square_size:  # If square_size computed before
            return self.calculated_square_size

        bbox_area = self.get_bbox_area()
        if bbox_area < CLUSTERING["square_size"][0] ** 2 * CLUSTERING_DENCITY:
            self.calculated_square_size = False
            return False

        for i in range(1, len(CLUSTERING["square_size"])):
            if bbox_area < CLUSTERING["square_size"][i] ** 2 * CLUSTERING_DENCITY:
                self.calculated_square_size = CLUSTERING["square_size"][i - 1]
                return self.calculated_square_size

        self.calculated_square_size = CLUSTERING["square_size"][
            len(CLUSTERING["square_size"]) - 1
        ]
        return self.calculated_square_size


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
