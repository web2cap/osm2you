from core.models.stories import Story
from rest_framework.viewsets import ModelViewSet

from api.permissions import AuthorAdminOrInstanceOnly
from api.serializers.stories import (
    StorySerializer,
    StorySerializerDisplay,
    StorySerializerText,
)


class StoryViewSet(ModelViewSet):
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
