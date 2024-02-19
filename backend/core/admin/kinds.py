from django.contrib import admin

from core.models.kinds import Kind, KindGroup


@admin.register(KindGroup)
class KindGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "descriptive_name", "color", "icon")
    search_fields = ("name", "descriptive_name")


@admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display = ("tag", "value", "kind_group", "kind_class", "priority")
    search_fields = ("tag", "value")
    list_filter = ("kind_group", "kind_class", "priority")
