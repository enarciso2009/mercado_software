from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # app principal
    path("", include("softwares.urls")),

    #auth do Django (login / logout)
    path("accounts/", include("django.contrib.auth.urls")),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )