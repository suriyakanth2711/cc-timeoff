from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse

# ... the rest of your URLconf goes here ...




schema_view = get_schema_view(
    openapi.Info(
        title="timeoff API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("",lambda x: HttpResponse( "Timeoff\n Works :) refer    https://github.com/suriyakanth2711/cc-timeoff")),
    path('admin/', admin.site.urls),
    path('api/timeoff/', include('timeoff_api.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
]

urlpatterns += staticfiles_urlpatterns()
