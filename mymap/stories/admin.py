from django.contrib import admin

from .models import Story


class StoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "created", "author", "marker")
    search_fields = ("text",)
    list_filter = ("created",)
    list_editable = ("marker",)
    empty_value_display = "-none-"


admin.site.register(Story, StoryAdmin)
