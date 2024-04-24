from django.urls import path, include
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import TemplateView

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include('api.urls')),
    path('', TemplateView.as_view(template_name="index.html"), name="index")
]
