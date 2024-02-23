from django.contrib import admin

from core.models.tags import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "display_name", "created")
    search_fields = ("name", "display_name")
