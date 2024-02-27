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

    @staticmethod
    def get_tags_all():
        return Tag.objects.all()


class TagStoreService:
    def __init__(self):
        self.tags = {}
        tags = TagService.get_tags_all()
        for tag in tags:
            self.tags[tag.name] = tag

    def get_or_create_tag(self, name):
        if name in self.tags:
            return self.tags[name], False
        else:
            tag, created = TagService.get_or_create_tag(name)
            self.tags[name] = tag
            return tag, created
