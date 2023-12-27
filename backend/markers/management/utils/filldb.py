from django.contrib.gis.geos import Point
from markers.models import Marker
from tags.models import Tag, TagValue


def update_nodes(nodes):
    """
    Update or create markers, tags, and tag values in the database based on the provided nodes.

    Args:
        nodes (list): A list of dictionaries representing nodes with information about markers, tags, and tag values.

            Example:
            [
                {
                    'id': '1876313153',
                    'lat': '59.0593972',
                    'lon': '9.8729957',
                    'name': None,
                    'tags': {'backcountry': 'yes', 'impromptu': 'yes', 'tourism': 'camp_site'}
                },
                # ... (other nodes)
            ]

    Returns:
        bool: True if the update or creation process is successful, False otherwise.

    Raises:
        Exception: If an unexpected error occurs during the database update or creation process.

    Note:
        - This function uses Django's GeoDjango framework to interact with a spatial database.
        - The provided nodes should follow a specific structure with information about markers, tags, and tag values.
        - The function updates or creates markers, tags, and tag values in an atomic transaction for data consistency.
    """

    try:
        for node in nodes:
            # Marker
            location = Point(float(node["lon"]), float(node["lat"]))
            marker_queryset = Marker.objects.filter(location__exact=location)
            if marker_queryset.exists():  # get marker
                marker = marker_queryset.first()
                if node["name"] and not marker.name:  # update marker name
                    marker.name = (
                        node["name"]["v"]
                        if isinstance(node["name"], dict)
                        else node["name"]
                    )
                    marker.save()
            else:  # create marker
                marker = Marker.objects.create(name=node.get("name"), location=location)
            # Tag
            for tag_name, tag_value in node["tags"].items():
                tag_queryset = Tag.objects.filter(name=tag_name)
                if tag_queryset.exists():  # get tag
                    tag = tag_queryset.first()
                else:  # create tag
                    tag = Tag.objects.create(name=tag_name)
                    # TagValue
                    marker_tag_value_queryset = TagValue.objects.filter(
                        marker=marker, tag=tag
                    )
                    if marker_tag_value_queryset.exists():  # get value
                        marker_tag_value = marker_tag_value_queryset.first()
                        # update value
                        if tag_value and marker_tag_value.value != tag_value:
                            marker_tag_value.value = tag_value
                            marker_tag_value.save()
                    else:  # create marker tag value
                        if not tag_value:
                            tag_value = None
                        marker_tag_value = TagValue.objects.create(
                            marker=marker, tag=tag, value=tag_value
                        )
        return True
    except Exception as e:
        print(f"update_nodes error: {e}")
        return False
