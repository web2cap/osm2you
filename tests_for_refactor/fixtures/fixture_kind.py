import pytest
from tags.models import Kind, KindGroup


@pytest.fixture
def main_kind_group_data():
    return {
        "name": "main_kind_group",
        "descriptive_name": "Main kind group name display",
    }


@pytest.fixture
def main_kind_group(main_kind_group_data):
    return KindGroup.objects.create(**main_kind_group_data)


@pytest.fixture
def main_kind_data(main_kind_group, tourism_tag):
    return {
        "kind_group": main_kind_group,
        "tag": tourism_tag,
        "kind_class": Kind.KIND_CLASS_MAIN,
        "priority": 0,
        "value": "camp_site",
    }


@pytest.fixture
def main_kind(main_kind_data):
    return Kind.objects.create(**main_kind_data)
