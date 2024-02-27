from django.db import transaction

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
    def get_all_marker_tags_values(marker):
        marker_tag_values = TagValue.objects.filter(marker=marker)
        return marker_tag_values

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


class TagValueStoreService:
    def __init__(self, marker):
        self._marker_tags_values = {}
        self._for_creation_tags_values = []
        self._for_updating_tags_values = []
        self._marker = marker

        tags_values = TagService.get_all_marker_tags_values(marker)
        for tag_value in tags_values:
            self._marker_tags_values[tag_value.tag.name] = tag_value

    def check_tag_value(self, tag, value):
        if tag.name in self._marker_tags_values:
            if self._marker_tags_values[tag.name].value != value:
                self._for_updating_tags_values.append(
                    (self._marker_tags_values[tag.name], value)
                )
                return False, True
            return False, False
        self._for_creation_tags_values.append((tag, value))
        return True, False

    def commit_values(self):
        create = self._commit_creation_tags_values()
        update = self._commit_updating_tags_values()
        return create, update

    def _commit_creation_tags_values(self):
        create_tag_values = []
        for tag, value in self._for_creation_tags_values:
            tag_value = TagValue(marker=self._marker, tag=tag, value=value)
            create_tag_values.append(tag_value)
        TagValue.objects.bulk_create(create_tag_values)
        self._for_creation_tags_values.clear()
        return len(create_tag_values)

    def _commit_updating_tags_values(self):
        update_tag_values = []
        with transaction.atomic():
            for tag_value, value in self._for_updating_tags_values:
                tag_value.value = value
                update_tag_values.append(tag_value)
            result = TagValue.objects.bulk_update(update_tag_values, ["value"])
            self._for_updating_tags_values.clear()
        return result
