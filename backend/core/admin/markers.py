from django import forms
from django.contrib.gis import admin

from core.models.markers import Marker


@admin.register(Marker)
class MarkerAdmin(admin.GISModelAdmin):
    """Marker admin."""

    list_display = (
        "name",
        "location",
        "kind",
        "author",
        "add_date",
    )
    search_fields = (
        "name",
        "kind",
        "author__username",
        "author__first_name",
        "author__last_name",
    )
    list_filter = ("kind",)

    def get_form(self, request, obj=None, **kwargs):
        """Override the author field with the current user."""
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields["author"].initial = request.user.id
        return form
