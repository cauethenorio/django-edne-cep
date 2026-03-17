from django.contrib import admin
from django.urls import include, path
from views import cep_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cep/<str:cep>/", cep_view),
    path("htmx/", include("htmx.urls")),
]
