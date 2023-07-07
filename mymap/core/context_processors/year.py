from django.utils import timezone


def year(request):
    """Add current year."""

    now = timezone.now()
    return {"year": now.year}
