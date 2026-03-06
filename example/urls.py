from django.urls import path
from views import cep_view

urlpatterns = [
    path("cep/<str:cep>/", cep_view),
]
