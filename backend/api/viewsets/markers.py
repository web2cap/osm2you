from core.services.bbox_square import BboxSquare
from core.services.kinds import KindService
from core.services.marker_clusters import MarkerClusterService
from core.services.markers import MarkerService
from core.services.related_markers import RelatedMarkers
from core.services.users import UserService
from core.tasks import run_scrap_markers_related
from django.conf import settings
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
        return self.get_all_queryset()

    def get_all_queryset(self):
        return MarkerService.get_markers_all()

    def get_list_queryset(self):
        """Get the queryset for Marker objects with main kind class only for the 'list' action."""
        return MarkerService.get_markers_main_kind()

    def get_retrieve_queryset(self):
        """Get the queryset for Marker objects with additional related data for the 'retrieve' action."""
        return MarkerService.get_markers_with_stories_tags()

    def get_cluster_queryset(self):
        """Get the queryset for MarkerCluster objects based on the current square size."""

        return MarkerClusterService.get_clusters_by_size(
            self.bbox_square_service.get_square_size()
        )

    def get_user_markers_queryset(self, user):
        """Get the queryset for markers associated with a specific user and their stories."""
        return MarkerService.get_users_markers_stories(user)

    def perform_create(self, serializer):
        """Add the authorized user to the author field during marker creation.
        Add tag value with main kind for creating marker.
        After creation initialize scrap_markers_related task for the marker."""

        serializer.save(author=self.request.user)
        KindService.set_marker_main_kind(marker=serializer.instance)
        run_scrap_markers_related.delay(serializer.instance.id)

    def perform_update(self, serializer):
        """If location changed, initialize scrap_markers_related task for the marker."""

        old_marker = MarkerService.get_by_id(serializer.instance.pk)
        serializer.save()
        new_location = serializer.validated_data.get("location")
        if new_location and old_marker.location != new_location:
            run_scrap_markers_related.delay(serializer.instance.id)

    @action(methods=["get"], detail=False, url_path="user/(?P<username>[^/.]+)")
    def user(self, request, username):
        """Check if a username exists, get the user, and add user info to the response.
        Add markers with users stories and users markers."""

        user = UserService.get_by_username(username)
        user_data = {"user": CustomUserInfoSerializer(user).data}

        markers_queryset = self.filter_queryset(self.get_user_markers_queryset(user))
        markers_data = self.get_serializer(markers_queryset, many=True).data

        return Response(user_data | markers_data)
