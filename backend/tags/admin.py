from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "display_name", "created")
    search_fields = ("name", "display_name")


admin.site.register(Tag, TagAdmin)
