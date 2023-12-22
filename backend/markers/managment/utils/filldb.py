from django.contrib.gis.geos import Point
from markers.models import Marker
from tags.models import Tag, TagValue


def update_nodes(nodes):
    try:
        for node in nodes:
            # Marker
            location = Point(node["lat"], node["lon"])
            marker_queryset = Marker.objects.filter(location__exact=location)
            if marker_queryset.exists():  # get marker
                marker = marker_queryset.first()
                if node["name"] and not marker.name:  # update marker name
                    marker.update(name=node["name"])
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
                            marker_tag_value.update(value=tag_value)
                    else:  # create marker tag value
                        marker_tag_value = TagValue.objects.create(
                            marker=marker, value=tag_value
                        )
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
