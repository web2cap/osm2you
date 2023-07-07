from django.urls import path

from .views import index, markersdetail, profile, storydetail

app_name = "markers"

urlpatterns = [
    path("", index, name="index"),
    path("marker/<int:marker_id>/", markersdetail, name="detail"),
    path("profile/", profile, name="myprofile"),
    path("profile/<str:username>/", profile, name="profile"),
    path("story/<int:story_id>/", storydetail, name="story_detail"),
]

# TODO:
""" 
    path(
        "profile/<str:username>/follow/",
        views.profile_follow,
        name="profile_follow",
    ),
    path(
        "profile/<str:username>/unfollow/",
        views.profile_unfollow,
        name="profile_unfollow",
    ),
"""
