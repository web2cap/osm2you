from drf_yasg import openapi

api_info = openapi.Info(
    title="osm2you API",
    default_version="v1",
    description="drf-yasg API docs",
    terms_of_service="https://github.com/web2cap/osm2you/blob/main/LICENSE",
    contact=openapi.Contact(email=""),
    license=openapi.License(name="BSD License"),
)
