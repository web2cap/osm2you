from django.db import transaction

from core.models.tag_values import TagValue
from core.models.tags import Tag


class TagService:
    @staticmethod
    def get_or_create_tag(tag_name, tag_display_name=None):
        """
        Get or create a tag with the given name.

        Returns:
            Tag: The tag instance.
            bool: True if the tag was created, False otherwise.
        """
        tag, created = Tag.objects.get_or_create(
            name=tag_name, defaults={"display_name": tag_display_name}
        )
        return tag, created

    @staticmethod
    def update_or_create_tag_value(tag, tag_value, marker):
        """
        Update or create a tag value for the given tag, tag value and marker.

        Returns:
            TagValue: The tag value instance.
            bool: True if the tag value was created, False otherwise.
        """
        marker_tag_value, created = TagValue.objects.get_or_create(
            marker=marker, tag=tag, defaults={"value": tag_value}
        )
        return marker_tag_value, created

    @staticmethod
    def get_all_marker_tags_values(marker):
        """Get all tag values associated with the given marker."""
        return TagValue.objects.filter(marker=marker)

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
        """
        Get or create a tag with the given name.

        Args:
            name (str): The name of the tag.

        Returns:
            Tag: The tag instance.
            bool: True if the tag was created, False otherwise.
        """
        if name in self.tags:
            return self.tags[name], False
        else:
            tag, created = TagService.get_or_create_tag(name)
            self.tags[name] = tag
            return tag, created


class TagValueStoreService:
    def __init__(self, marker):
        """
        Initialize the tag value store service.

        Args:
            marker: The marker instance.
        """
        self._marker_tags_values = {}
        self._for_creation_tags_values = []
        self._for_updating_tags_values = []
        self._marker = marker

        tags_values = TagService.get_all_marker_tags_values(marker)
        for tag_value in tags_values:
            self._marker_tags_values[tag_value.tag.name] = tag_value

    def check_tag_value(self, tag, value):
        """
        Check if the tag value needs to be created or updated.

        Args:
            tag (Tag): The tag instance.
            value (str): The value of the tag.

        Returns:
            tuple: A tuple containing a boolean indicating if the tag value needs to be created,
                   and a boolean indicating if the tag value needs to be updated.
        """
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
        """
        Commit the tag values to the database.

        Returns:
            tuple: A tuple containing the number of tag values created and the result of updating tag values.
        """
        create = self._commit_creation_tags_values()
        update = self._commit_updating_tags_values()
        return create, update

    def _commit_creation_tags_values(self):
        """
        Commit the creation of tag values to the database.

        Returns:
            int: The number of tag values created.
        """
        create_tag_values = []
        for tag, value in self._for_creation_tags_values:
            tag_value = TagValue(marker=self._marker, tag=tag, value=value)
            create_tag_values.append(tag_value)
        TagValue.objects.bulk_create(create_tag_values)
        self._for_creation_tags_values.clear()
        return len(create_tag_values)

    def _commit_updating_tags_values(self):
        """
        Commit the updating of tag values to the database.

        Returns:
            int: The number of tag values updated.
        """
        update_tag_values = []
        with transaction.atomic():
            for tag_value, value in self._for_updating_tags_values:
                tag_value.value = value
                update_tag_values.append(tag_value)
            result = TagValue.objects.bulk_update(update_tag_values, ["value"])
            self._for_updating_tags_values.clear()
        return result
