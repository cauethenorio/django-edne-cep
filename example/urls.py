from django.contrib import admin
from django.urls import path
from views import cep_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cep/<str:cep>/", cep_view),
]
