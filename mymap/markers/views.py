import json

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, render

from stories.models import Story
from stories.utils import paginations
from users.models import User

from .models import Marker


def index(request):
    """Markers map view."""

    template_name = "markers/index.html"

    context = {
        "markers": json.loads(serialize("geojson", Marker.objects.all())),
    }

    return render(request, template_name, context)


def markersdetail(request, marker_id):
    """Marker detail with stories"""

    template_name = "markers/detail.html"

    marker = get_object_or_404(Marker, pk=marker_id)
    markers = json.loads(serialize("geojson", (marker,)))
    story_list = marker.stories.all()
    page_obj = paginations(request, story_list)

    context = {
        "title": f"Place: {marker.name}",
        "page_obj": page_obj,
        "story_list": story_list,
        "marker": marker,
        "markers": markers,
    }
    return render(request, template_name, context)


@login_required(login_url="users:login")
def profile(request, username=None):
    "Просмотр профиля пользователя."

    template = "markers/profile.html"

    if not username:
        username = request.user.username
    user = get_object_or_404(User, username=username)
    markers = json.loads(serialize("geojson", user.markers.all()))
    story_list = user.stories.all()
    page_obj = paginations(request, story_list)

    context = {
        "page_obj": page_obj,
        "story_list": story_list,
        "profile": user,
        "markers": markers,
    }
    return render(request, template, context)


def storydetail(request, story_id):
    """Story with marker"""

    template_name = "markers/story_detail.html"

    story = get_object_or_404(Story, pk=story_id)
    markers = json.loads(serialize("geojson", (story.marker,)))

    context = {
        "story": story,
        "markers": markers,
    }
    return render(request, template_name, context)
