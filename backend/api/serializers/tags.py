from core.models.tags import Kind, Tag
from rest_framework import serializers


class KindSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source="kind_group.color", read_only=True)
    icon = serializers.CharField(source="kind_group.icon", read_only=True)
    tag = serializers.CharField(source="tag.name", read_only=True)
    tag_display_name = serializers.CharField(source="tag.display_name", read_only=True)
    kind = serializers.SerializerMethodField()

    def get_kind(self, obj):
        return f"{obj.tag.name}={obj.value}"

    class Meta:
        model = Kind
        fields = ("tag", "tag_display_name", "value", "color", "icon", "kind")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
            "display_name",
        )
