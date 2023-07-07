from django.conf import settings
from django.core.paginator import Paginator

STORY_PER_PAGE = getattr(settings, "STORY_PER_PAGE", None)


def paginations(request, data_list):
    """Pagination."""

    paginator = Paginator(data_list, STORY_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return page_obj
