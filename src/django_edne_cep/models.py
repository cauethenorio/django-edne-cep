from django.db import models

from .table_names import get_table_name


class Cep(models.Model):
    cep = models.CharField(max_length=8, primary_key=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=72, null=True, blank=True)
    municipio = models.CharField(max_length=72)
    municipio_cod_ibge = models.IntegerField()
    uf = models.CharField(max_length=2)
    nome = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = get_table_name("cep_unificado")

    def __str__(self) -> str:
        return f"{self.cep[:5]}-{self.cep[5:]}"
