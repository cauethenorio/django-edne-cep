"""
Main CEP model (unified/denormalized table).

Field definitions based on edne-correios-loader:
https://github.com/cauethenorio/edne-correios-loader/blob/main/src/edne_correios_loader/tables.py
"""

from django.db import models

from .table_names import get_table_name


class Cep(models.Model):
    """Tabela unificada de CEP."""

    cep = models.CharField("CEP", max_length=8, primary_key=True)
    logradouro = models.CharField("logradouro", max_length=100, null=True, blank=True)
    complemento = models.CharField("complemento", max_length=100, null=True, blank=True)
    bairro = models.CharField("bairro", max_length=72, null=True, blank=True)
    municipio = models.CharField("município", max_length=72)
    municipio_cod_ibge = models.IntegerField("código do município IBGE")
    uf = models.CharField("UF", max_length=2)
    nome = models.CharField("nome", max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("cep_unificado")
        verbose_name = "CEP"
        verbose_name_plural = "CEPs"

    def __str__(self) -> str:
        return f"{self.cep[:5]}-{self.cep[5:]}"
