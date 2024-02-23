from core.models.stories import Story
from rest_framework import serializers

from api.serializers.users import CustomUserShortSerializer


class StorySerializer(serializers.ModelSerializer):
    """Stories serializer."""

    def validate_text(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Text must be at least 10 characters long."
            )
        return value

    class Meta:
        model = Story
        fields = ("id", "text", "author", "marker")
        read_only_fields = ("id", "author")


class StorySerializerText(serializers.ModelSerializer):
    """Stories serializer for edit. Enable edit text."""

    def validate_text(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError(
                "Text must be at least 10 characters long."
            )
        return value

    class Meta:
        model = Story
        fields = ("text", "created")
        read_only_fields = ("created",)


class StorySerializerDisplay(serializers.ModelSerializer):
    """Extendet stories serializer with aditional user info.
    Field is_yours True for owners of record.
    Field marker excludet."""

    author = CustomUserShortSerializer(many=False, read_only=True)
    is_yours = serializers.SerializerMethodField()

    def get_is_yours(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.author_id == request.user.id
        return False

    class Meta:
        model = Story
        fields = ("id", "text", "author", "is_yours", "created")
