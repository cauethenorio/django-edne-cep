from django.contrib import admin
from django.contrib.admin import AdminSite

from django_edne_cep.admin import ReadOnlyAdmin, _related_link
from django_edne_cep.settings import get_setting


# readonly_fields with link_* methods show clickable links to related
# model lists on the detail page, avoiding heavy inlines for large datasets
class LocalidadeAdmin(ReadOnlyAdmin):
    list_display = ("loc_nu", "loc_no", "loc_in_tipo_loc", "ufe_sg", "cep_formatado")
    search_fields = ("loc_no", "cep")
    list_filter = ("ufe_sg", "loc_in_tipo_loc")
    readonly_fields = (
        "link_logradouros",
        "link_bairros",
        "link_caixas_postais",
        "link_grandes_usuarios",
        "link_unidades_operacionais",
        "link_subordinadas",
    )

    @admin.display(description="Logradouros")
    def link_logradouros(self, obj: object) -> str:
        c = obj.logradouro_set.count()
        return _related_link(
            obj, "logradouro", "loc_nu", "logradouro", "logradouros", c
        )

    @admin.display(description="Bairros")
    def link_bairros(self, obj: object) -> str:
        c = obj.bairro_set.count()
        return _related_link(obj, "bairro", "loc_nu", "bairro", "bairros", c)

    @admin.display(description="Caixas postais comunitárias")
    def link_caixas_postais(self, obj: object) -> str:
        c = obj.caixapostalcomunitaria_set.count()
        return _related_link(
            obj, "caixapostalcomunitaria", "loc_nu", "caixa postal", "caixas postais", c
        )

    @admin.display(description="Grandes usuários")
    def link_grandes_usuarios(self, obj: object) -> str:
        c = obj.grandeusuario_set.count()
        return _related_link(
            obj, "grandeusuario", "loc_nu", "grande usuário", "grandes usuários", c
        )

    @admin.display(description="Unidades operacionais")
    def link_unidades_operacionais(self, obj: object) -> str:
        c = obj.unidadeoperacional_set.count()
        return _related_link(
            obj,
            "unidadeoperacional",
            "loc_nu",
            "unidade operacional",
            "unidades operacionais",
            c,
        )

    @admin.display(description="Localidades subordinadas")
    def link_subordinadas(self, obj: object) -> str:
        c = obj.localidade_set.count()
        return _related_link(
            obj, "localidade", "loc_nu_sub", "subordinada", "subordinadas", c
        )


class BairroAdmin(ReadOnlyAdmin):
    list_display = ("bai_nu", "bai_no", "loc_nu", "ufe_sg")
    search_fields = ("bai_no",)
    list_filter = ("ufe_sg",)
    readonly_fields = (
        "link_logradouros",
        "link_grandes_usuarios",
        "link_unidades_operacionais",
    )

    @admin.display(description="Logradouros")
    def link_logradouros(self, obj: object) -> str:
        c = obj.logradouro_set.count()
        return _related_link(
            obj, "logradouro", "bai_nu_ini", "logradouro", "logradouros", c
        )

    @admin.display(description="Grandes usuários")
    def link_grandes_usuarios(self, obj: object) -> str:
        c = obj.grandeusuario_set.count()
        return _related_link(
            obj, "grandeusuario", "bai_nu", "grande usuário", "grandes usuários", c
        )

    @admin.display(description="Unidades operacionais")
    def link_unidades_operacionais(self, obj: object) -> str:
        c = obj.unidadeoperacional_set.count()
        return _related_link(
            obj,
            "unidadeoperacional",
            "bai_nu",
            "unidade operacional",
            "unidades operacionais",
            c,
        )


class LogradouroAdmin(ReadOnlyAdmin):
    list_display = ("log_nu", "log_no", "cep_formatado", "tlo_tx", "loc_nu", "ufe_sg")
    # loc_nu__loc_no allows searching logradouros by city name
    search_fields = ("log_no", "cep", "loc_nu__loc_no")
    list_filter = ("ufe_sg",)
    readonly_fields = ("link_grandes_usuarios", "link_unidades_operacionais")

    @admin.display(description="Grandes usuários")
    def link_grandes_usuarios(self, obj: object) -> str:
        c = obj.grandeusuario_set.count()
        return _related_link(
            obj, "grandeusuario", "log_nu", "grande usuário", "grandes usuários", c
        )

    @admin.display(description="Unidades operacionais")
    def link_unidades_operacionais(self, obj: object) -> str:
        c = obj.unidadeoperacional_set.count()
        return _related_link(
            obj,
            "unidadeoperacional",
            "log_nu",
            "unidade operacional",
            "unidades operacionais",
            c,
        )


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


CEP_TABLES_ADMINS = {
    "Localidade": LocalidadeAdmin,
    "Bairro": BairroAdmin,
    "Logradouro": LogradouroAdmin,
    "CaixaPostalComunitaria": CaixaPostalComunitariaAdmin,
    "GrandeUsuario": GrandeUsuarioAdmin,
    "UnidadeOperacional": UnidadeOperacionalAdmin,
}


def register_cep_tables_admin(site: AdminSite | None = None) -> None:
    if not get_setting("ADMIN_ENABLED"):
        return

    from . import models as cep_models  # noqa: PLC0415

    site = site or admin.site
    for model_name, admin_class in CEP_TABLES_ADMINS.items():
        model = getattr(cep_models, model_name)
        site.register(model, admin_class)


register_cep_tables_admin()
