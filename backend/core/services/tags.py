from core.models.tags import Tag, TagValue


class TagService:
    @staticmethod
    def get_or_create_tag(tag_name, tag_display_name=None):
        tag, created = Tag.objects.get_or_create(
            name=tag_name, defaults={"display_name": tag_display_name}
        )
        return tag, created

    @staticmethod
    def update_or_create_tag_value(tag, tag_value, marker):
        marker_tag_value, created = TagValue.objects.get_or_create(
            marker=marker, tag=tag, defaults={"value": tag_value}
        )
        return marker_tag_value, created
