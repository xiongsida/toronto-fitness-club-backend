from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Toronto Fitness Club API",
        default_version='1.0.0',
        description="API documentation",
    ),
    public=True,
)

swagger_urls = [
    path('document', schema_view.with_ui('swagger',
         cache_timeout=0), name="swagger-schema"),
]
