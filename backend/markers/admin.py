from django.contrib.gis import admin

from .models import Marker


@admin.register(Marker)
class MarkerAdmin(admin.GISModelAdmin):
    """Marker admin."""

    list_display = ("name", "kind", "location", "author", "add_date")
    list_filter = ("kind",)
    search_fields = (
        "name",
        "author__username",
        "author__first_name",
        "author__last_name",
    )

    def get_form(self, request, obj=None, **kwargs):
        """Override the author field with the current user."""
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields["author"].initial = request.user.id
        return form
