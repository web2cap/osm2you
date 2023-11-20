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
    StorySerializer,
    StorySerializerDisplay,
    StorySerializerEdit,
)


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker view set."""

    permission_classes = (AuthorAdminOrReadOnly,)

    bbox_filter_field = "location"
    filter_backends = (filters.InBBoxFilter,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MarkerInstanceSerializer
        elif self.action == "user":
            # todo serializer
            pass
        return MarkerSerializer

    def get_queryset(self):
        queryset = Marker.objects.all()
        if self.action in ("retrieve", "user"):
            queryset = queryset.prefetch_related(
                Prefetch(
                    "stories",
                    queryset=Story.objects.select_related("author"),
                ),
                "stories__author",
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["get"], detail=False, url_path="user/(?P<username>[^/.]+)")
    def user(self, request, username):
        user = get_object_or_404(User, username=username)
        queryset = (
            self.get_queryset()
            .filter(Q(author=user) | Q(stories__author=user))
            .distinct()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StoryViewSet(viewsets.ModelViewSet):
    """Story view set."""

    queryset = Story.objects.select_related("author").all()
    serializer_class = StorySerializer
    permission_classes = (AuthorAdminOrInstanceOnly,)
    serializers = {
        "list": StorySerializerDisplay,
        "retrieve": StorySerializerDisplay,
        "partial_update": StorySerializerEdit,
        "default": StorySerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers["default"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
