from django.contrib import admin

from .models import Kind, KindGroup, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "display_name", "created")
    search_fields = ("name", "display_name")


class KindGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "descriptive_name")
    search_fields = ("name", "descriptive_name")


admin.site.register(Tag, TagAdmin)
admin.site.register(KindGroup, KindGroupAdmin)
