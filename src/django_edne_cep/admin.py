import contextlib
import re

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from .models import Cep
from .settings import get_setting

# match CEP with or without hyphen so we can normalize before searching
_CEP_RE = re.compile(r"^\d{5}-?\d{3}$")


def _format_cep(cep: str | None) -> str:
    return f"{cep[:5]}-{cep[5:]}" if cep else ""


def _related_link(
    obj: object,
    model_name: str,
    fk_field: str,
    singular: str,
    plural: str,
    count: int,
) -> str:
    if count == 0:
        return f"Nenhum {singular}"
    url = reverse(f"admin:django_edne_cep_{model_name}_changelist")
    label = f"Ver {count} {singular if count == 1 else plural}"
    return format_html('<a href="{}?{}={}">{}</a>', url, fk_field, obj.pk, label)


class NullFieldFilter(admin.SimpleListFilter):  # type: ignore[type-arg]
    """
    Filter for nullable/blank fields: has value vs empty

    Checks both None and "" because CharField stores blanks as empty strings
    """

    field_name: str = ""

    def lookups(
        self,
        request: HttpRequest,
        model_admin: admin.ModelAdmin,  # type: ignore[type-arg]
    ) -> list[tuple[str, str]]:
        return [("yes", "Sim"), ("no", "Não")]

    def queryset(
        self,
        request: HttpRequest,
        queryset: models.QuerySet,  # type: ignore[type-arg]
    ) -> models.QuerySet:  # type: ignore[type-arg]
        if self.value() == "yes":
            return queryset.exclude(**{self.field_name: ""}).exclude(
                **{self.field_name: None}
            )
        if self.value() == "no":
            return queryset.filter(
                models.Q(**{self.field_name: ""}) | models.Q(**{self.field_name: None})
            )
        return queryset


class TemLogradouroFilter(NullFieldFilter):
    title = "tem logradouro"
    parameter_name = "tem_logradouro"
    field_name = "logradouro"


class TemBairroFilter(NullFieldFilter):
    title = "tem bairro"
    parameter_name = "tem_bairro"
    field_name = "bairro"


# eDNE data is loaded externally, so all admins are read-only
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

    @admin.display(description="CEP", ordering="cep")
    def cep_formatado(self, obj: object) -> str:
        return _format_cep(getattr(obj, "cep", ""))


class CepAdmin(ReadOnlyAdmin):
    list_display = ("cep_formatado", "logradouro", "bairro", "municipio", "uf")
    search_fields = ("cep", "logradouro", "bairro", "municipio")
    list_filter = ("uf", TemLogradouroFilter, TemBairroFilter)

    def get_search_results(self, request, queryset, search_term):  # type: ignore[override]
        # strip hyphen only when term looks like a CEP to avoid breaking
        # searches for street names with hyphens (e.g. "Ana-Rosa")
        term = search_term.strip()
        if _CEP_RE.match(term):
            term = term.replace("-", "")
        return super().get_search_results(request, queryset, term)


def register_admin(site: AdminSite | None = None) -> None:
    if not get_setting("ADMIN_ENABLED"):
        return

    site = site or admin.site
    with contextlib.suppress(AlreadyRegistered):
        site.register(Cep, CepAdmin)


register_admin()
