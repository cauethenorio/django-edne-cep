from django.apps import apps
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpRequest

from .models import Cep
from .settings import get_setting


def _format_cep(cep: str) -> str:
    return f"{cep[:5]}-{cep[5:]}" if cep else ""


class ReadOnlyAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    def has_add_permission(
        self, request: HttpRequest | None, obj: object = None
    ) -> bool:
        return False

    def has_change_permission(
        self, request: HttpRequest | None, obj: object = None
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest | None, obj: object = None
    ) -> bool:
        return False

    @admin.display(description="CEP")
    def cep_formatado(self, obj: object) -> str:
        return _format_cep(getattr(obj, "cep", ""))


class CepAdmin(ReadOnlyAdmin):
    list_display = ("cep", "logradouro", "bairro", "municipio", "uf")
    search_fields = ("cep", "logradouro", "bairro", "municipio")
    list_filter = ("uf",)


class LocalidadeAdmin(ReadOnlyAdmin):
    list_display = ("loc_nu", "loc_no", "ufe_sg", "cep_formatado")
    search_fields = ("loc_no", "cep")
    list_filter = ("ufe_sg", "loc_in_tipo_loc")


class BairroAdmin(ReadOnlyAdmin):
    list_display = ("bai_nu", "bai_no", "ufe_sg")
    search_fields = ("bai_no",)
    list_filter = ("ufe_sg",)


class LogradouroAdmin(ReadOnlyAdmin):
    list_display = ("log_nu", "log_no", "cep_formatado", "tlo_tx", "ufe_sg")
    search_fields = ("log_no", "cep")
    list_filter = ("ufe_sg",)


class CaixaPostalComunitariaAdmin(ReadOnlyAdmin):
    list_display = ("cpc_nu", "cpc_no", "cep_formatado", "ufe_sg")
    search_fields = ("cpc_no", "cep")
    list_filter = ("ufe_sg",)


class GrandeUsuarioAdmin(ReadOnlyAdmin):
    list_display = ("gru_nu", "gru_no", "cep_formatado", "ufe_sg")
    search_fields = ("gru_no", "cep")
    list_filter = ("ufe_sg",)


class UnidadeOperacionalAdmin(ReadOnlyAdmin):
    list_display = ("uop_nu", "uop_no", "cep_formatado", "ufe_sg")
    search_fields = ("uop_no", "cep")
    list_filter = ("ufe_sg",)


_CEP_TABLES_ADMINS = {
    "Localidade": LocalidadeAdmin,
    "Bairro": BairroAdmin,
    "Logradouro": LogradouroAdmin,
    "CaixaPostalComunitaria": CaixaPostalComunitariaAdmin,
    "GrandeUsuario": GrandeUsuarioAdmin,
    "UnidadeOperacional": UnidadeOperacionalAdmin,
}


def register_admin(site: AdminSite | None = None) -> None:
    if not get_setting("ADMIN_ENABLED"):
        return

    site = site or admin.site
    site.register(Cep, CepAdmin)

    if apps.is_installed("django_edne_cep.cep_tables"):
        from .cep_tables import models as cep_models  # noqa: PLC0415

        for model_name, admin_class in _CEP_TABLES_ADMINS.items():
            model = getattr(cep_models, model_name)
            site.register(model, admin_class)


register_admin()
