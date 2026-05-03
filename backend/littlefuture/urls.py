from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# French admin branding
admin.site.site_header = "Little Future — Administration"
admin.site.site_title = "Little Future"
admin.site.index_title = "Tableau d'administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    # Server-rendered French pages
    path("", include("apps.core.urls")),
    # REST API
    path("api/v1/", include("apps.core.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
