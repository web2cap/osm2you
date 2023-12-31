import pytest
from tags.models import Tag


@pytest.fixture
def simple_tag_data():
    return {
        "name": "tagname",
        "display_name": "Tage name display",
    }


@pytest.fixture
def simple_tag(simple_tag_data):
    return Tag.objects.create(**simple_tag_data)


@pytest.fixture
def simple_tag_value_data(simple_marker, simple_tag):
    return {
        "tag": simple_tag,
        "marker": simple_marker,
        "value": "tagvalue example",
    }
