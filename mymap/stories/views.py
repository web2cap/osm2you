from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from markers.models import Marker
from users.models import User

from .forms import StoryDropForm, StoryForm
from .models import Story

# TODO:
# from django.views.decorators.cache import cache_page


@login_required(login_url="users:login")
def story_create(request, marker_id=None):
    """Add story"""

    template = "stories/create.html"

    form = StoryForm(request.POST or None)
    if form.is_valid():
        marker = get_object_or_404(Marker, pk=marker_id)
        instance = form.save(commit=False)
        instance.author_id = request.user.id
        instance.marker_id = marker.pk
        instance.save()
        return redirect("markers:detail", marker.pk)

    return render(request, template, {"form": form})


@login_required(login_url="users:login")
def story_edit(request, story_id):
    """Story edit, only for author permit."""

    template = "stories/create.html"

    story = get_object_or_404(Story, pk=story_id)

    if request.user.id != story.author.id:
        return redirect("markers:story_detail", story.pk)

    form = StoryForm(request.POST or None, instance=story)
    if form.is_valid():
        form.save()
        return redirect("markers:story_detail", story.pk)

    context = {
        "form": form,
        "is_edit": True,
    }
    return render(request, template, context)


@login_required(login_url="users:login")
def story_drop(request, story_id):
    """Story drop, only for author permit."""

    template = "stories/drop.html"

    story = get_object_or_404(Story, pk=story_id)
    if request.user.id != story.author.id:
        return redirect("markers:story_detail", story.pk)

    if "confirm" in request.POST and request.POST["confirm"] == "on":
        story.delete()
        return redirect("markers:myprofile")

    form = StoryDropForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, template, context)


# TODO
"""
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
   

    user = get_object_or_404(User, username=request.user)

    followed_people = Follow.objects.filter(user=user).values("author")
    post_list = Post.objects.filter(author__in=followed_people)
    page_obj = paginations(request, post_list)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "posts/follow.html", context)


@login_required
def profile_follow(request, username):
   

    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)

    return redirect("posts:profile", username)


@login_required
def profile_unfollow(request, username):
    

    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()

    return redirect("posts:profile", username)
"""
