from core.models.kinds import Kind
from core.models.tags import Tag
from rest_framework.viewsets import ModelViewSet

from api.permissions import ListOnly
from api.serializers.tags import KindSerializer, TagSerializer


class KindViewSet(ModelViewSet):
    """Kind group view set."""

    queryset = Kind.objects.select_related("kind_group").prefetch_related("tag")
    permission_classes = (ListOnly,)
    serializer_class = KindSerializer


class TagViewSet(ModelViewSet):
    """Kind group view set."""

    queryset = Tag.objects.all()
    permission_classes = (ListOnly,)
    serializer_class = TagSerializer
