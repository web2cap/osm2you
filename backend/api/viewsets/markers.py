from core.models.markers import Marker, MarkerCluster
from core.models.stories import Story
from core.models.tags import Kind, MarkerKind, TagValue
from core.models.users import User
from core.services.bbox_square import BboxSquare
from core.services.related_markers import RelatedMarkers
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
    MarkerSerializer,
    MarkerUserSerializer,
)
from api.serializers.users import CustomUserInfoSerializer

MARKERS_RELATED_IN_RADIUS = getattr(settings, "MARKERS_RELATED_IN_RADIUS", 5000)


class MarkerViewSet(ModelViewSet):
    """ViewSet for handling Marker objects, including clustering logic."""

    def initial(self, request, *args, **kwargs):
        self.bbox_square_service = BboxSquare(request.query_params.get("in_bbox"))
        super().initial(request, *args, **kwargs)

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

        if self.action == "list" and self.bbox_square_service.get_show_clusters():
            return self.serializers.get("clusters")
        return self.serializers.get(self.action, self.serializers["default"])

    def get_serializer_context(self):
        """Includes related markers data for marker into context."""

        context = super().get_serializer_context()
        if self.action == "retrieve":
            marker = self.get_object()
            context["related_markers"] = RelatedMarkers.get_related_markers_data(marker)
        return context

    def get_queryset(self):
        """Get the queryset for Marker objects or MarkerCluster objects based on the action.
        List only markers with main kind klass."""

        if self.action == "retrieve":
            return self.get_retrieve_queryset()
        if self.action == "list":
            if self.bbox_square_service.get_show_clusters():
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
