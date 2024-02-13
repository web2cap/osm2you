from django.contrib import admin

from core.models.tags import Kind, KindGroup, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "display_name", "created")
    search_fields = ("name", "display_name")


@admin.register(KindGroup)
class KindGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "descriptive_name", "color", "icon")
    search_fields = ("name", "descriptive_name")


@admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display = ("tag", "value", "kind_group", "kind_class", "priority")
    search_fields = ("tag", "value")
    list_filter = ("kind_group", "kind_class", "priority")