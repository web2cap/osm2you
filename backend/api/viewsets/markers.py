from core.models.markers import Marker, MarkerCluster
from core.models.stories import Story
from core.models.tags import Kind, MarkerKind, Tag, TagValue
from core.models.users import User
from core.services.bbox_square import BboxSquare
from core.tasks import run_scrap_markers_related
from django.conf import settings
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_gis import filters

from api.permissions import AuthorAdminOrReadOnly
from api.serializers.markers import (
    MarkerClusterSerializer,
    MarkerInstanceSerializer,
    MarkerRelatedSerializer,
    MarkerSerializer,
    MarkerUserSerializer,
)
from api.serializers.users import CustomUserInfoSerializer

MARKERS_RELATED_IN_RADIUS = getattr(settings, "MARKERS_RELATED_IN_RADIUS", 5000)


class MarkerViewSet(ModelViewSet):
    """ViewSet for handling Marker objects, including clustering logic."""

    def __init__(self, **kwargs):
        self.bbox_square_service = BboxSquare(self.request.query_params.get("in_bbox"))
        super().__init__(**kwargs)

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
        """Get the appropriate serializer class based on the action.
        For list action get serializer class based on zoom."""

        if self.action == "list" and self.bbox_square_service.get_square_size():
            return self.serializers.get("clusters")
        return self.serializers.get(self.action, self.serializers["default"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "retrieve":
            context["related_markers"] = self.get_related_markers_data(
                self.get_object()
            )
        return context

    def get_queryset(self):
        """Get the queryset for Marker objects or MarkerCluster objects based on the action.
        List only markers with main kind klass."""

        if self.action == "retrieve":
            return self.get_retrieve_queryset()
        if self.action == "list":
            if self.bbox_square_service.get_square_size():
                return self.get_cluster_queryset()
            return self.get_list_queryset()
        return Marker.objects.all()

    def get_list_queryset(self):
        """Get the queryset for Marker objects with main kind class only for the 'retrieve' action."""

        return Marker.objects.filter(kind__kind__kind_class=Kind.KIND_CLASS_MAIN)

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

        return MarkerCluster.objects.filter(
            square_size=self.bbox_square_service.get_square_size()
        )

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

    def get_related_markers_data(self, marker):
        """Get related markers data for a given marker within a specified radius."""

        related_markers = self.get_related_markers_queryset(
            marker, MARKERS_RELATED_IN_RADIUS
        )
        return MarkerRelatedSerializer(related_markers, many=True).data

    def get_related_markers_queryset(self, marker, radius):
        """
        Get the queryset for related markers within a specified radius from a given marker.
        Each related marker includes additional information about its kind."""

        return (
            Marker.objects.filter(location__distance_lte=(marker.location, radius))
            .exclude(id=marker.id)
            .select_related("kind__kind")
            .prefetch_related(
                Prefetch(
                    "kind__kind__tag",
                    queryset=Tag.objects.only("name"),
                    to_attr="kind__kind",
                )
            )
        )

    def perform_create(self, serializer):
        """Add the authorized user to the author field during marker creation.
        Add tag value with main kind for creating marker.
        After creation initialize scrap_markers_related task for the marker."""

        serializer.save(author=self.request.user)

        MarkerKind.objects.update_or_create(
            marker=serializer.instance,
            defaults={
                "kind": Kind.objects.filter(kind_class=Kind.KIND_CLASS_MAIN)
                .order_by("priority")
                .first()
            },
        )

        run_scrap_markers_related.delay(serializer.instance.id)

    def perform_update(self, serializer):
        """If location changed, initialize scrap_markers_related task for the marker."""

        old_marker = get_object_or_404(Marker, pk=serializer.instance.pk)
        serializer.save()

        new_location = serializer.validated_data.get("location")
        if new_location and old_marker.location != new_location:
            run_scrap_markers_related.delay(serializer.instance.id)

    @action(methods=["get"], detail=False, url_path="user/(?P<username>[^/.]+)")
    def user(self, request, username):
        """Check if a username exists, get the user, and add user info to the response.
        Add markers with users stories and users markers."""

        user = get_object_or_404(User, username=username)
        user_data = {"user": CustomUserInfoSerializer(user).data}

        markers_queryset = self.filter_queryset(self.get_user_markers_queryset(user))
        markers_data = self.get_serializer(markers_queryset, many=True).data

        return Response(user_data | markers_data)
