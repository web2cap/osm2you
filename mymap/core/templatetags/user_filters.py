from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    """Addclass filter, which provide adding CSS class in a temaplate."""
    return field.as_widget(attrs={"class": css})
