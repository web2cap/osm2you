from django import forms
from django.contrib.gis import admin
from tags.models import Kind

from .models import Marker


class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = "__all__"

    kind = forms.ModelChoiceField(
        queryset=Kind.objects.all(),
        required=False,
        empty_label="---------",
        label="Marker Kind Value",
    )


@admin.register(Marker)
class MarkerAdmin(admin.GISModelAdmin):
    """Marker admin."""

    form = MarkerForm
    list_display = ("name", "location", "author", "add_date", "get_kind_display")
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

    def get_kind_display(self, obj):
        """Display the kind value in the admin list."""
        if obj.kind.exists():
            return ", ".join(str(kind) for kind in obj.kind.all())
        return " - "

    get_kind_display.short_description = "Kind"
    get_kind_display.admin_order_field = "kind"
