from django.urls import path

from .views import story_create, story_drop, story_edit

app_name = "stories"

urlpatterns = [
    path("<int:story_id>/", story_create, name="detail"),
    path("<int:story_id>/edit/", story_edit, name="edit"),
    path("<int:story_id>/drop/", story_drop, name="drop"),
    path("create/<int:marker_id>/", story_create, name="create"),
    # TODO:
    # path(
    #     "posts/<int:post_id>/comment/", views.add_comment, name="add_comment"
    # ),
]
