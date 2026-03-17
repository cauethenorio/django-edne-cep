from django.urls import path

from .views import PedidoView, cep_details

app_name = "htmx"

urlpatterns = [
    path("", PedidoView.as_view(), name="pedido"),
    path("cep/", cep_details, name="cep-details"),
]
