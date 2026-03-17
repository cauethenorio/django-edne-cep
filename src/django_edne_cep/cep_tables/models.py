"""
Models for the e-DNE CEP auxiliary tables (cep-tables set).

Field definitions based on edne-correios-loader:
https://github.com/cauethenorio/edne-correios-loader/blob/main/src/edne_correios_loader/tables.py
"""

from django.db import models

from django_edne_cep.table_names import get_table_name


class SituacaoLocalidade(models.TextChoices):
    NAO_CODIFICADA = "0", "Não codificada ao nível de logradouro"
    CODIFICADA = "1", "Codificada ao nível de logradouro"
    DISTRITO = "2", "Distrito ou povoado inserido na codificação"
    FASE_CODIFICACAO = "3", "Em fase de codificação ao nível de logradouro"


class TipoLocalidade(models.TextChoices):
    DISTRITO = "D", "Distrito"
    MUNICIPIO = "M", "Município"
    POVOADO = "P", "Povoado"


class SimNao(models.TextChoices):
    SIM = "S", "Sim"
    NAO = "N", "Não"


class Localidade(models.Model):
    """Municípios, distritos e povoados do Brasil."""

    loc_nu = models.AutoField("chave da localidade", primary_key=True)
    ufe_sg = models.CharField("sigla da UF", max_length=2)
    loc_no = models.CharField("nome da localidade", max_length=72)
    cep = models.CharField("CEP da localidade", max_length=8, null=True, blank=True)
    loc_in_sit = models.CharField(
        "situação da localidade", max_length=1, choices=SituacaoLocalidade.choices
    )
    loc_in_tipo_loc = models.CharField(
        "tipo de localidade", max_length=1, choices=TipoLocalidade.choices
    )
    loc_nu_sub = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        db_column="loc_nu_sub",
        verbose_name="localidade de subordinação",
        null=True,
        blank=True,
    )
    loc_no_abrev = models.CharField(
        "abreviatura do nome da localidade", max_length=36, null=True, blank=True
    )
    mun_nu = models.IntegerField("código do município IBGE", null=True, blank=True)

    class Meta:
        managed = False
        # app_label intentionally uses the main app name so all CEP models
        # are grouped under a single section in Django admin
        app_label = "django_edne_cep"
        db_table = get_table_name("log_localidade")

    def __str__(self) -> str:
        return f"{self.loc_no}/{self.ufe_sg}"


class Bairro(models.Model):
    """Bairros."""

    bai_nu = models.AutoField("chave do bairro", primary_key=True)
    ufe_sg = models.CharField("sigla da UF", max_length=2)
    loc_nu = models.ForeignKey(
        Localidade,
        models.DO_NOTHING,
        db_column="loc_nu",
        verbose_name="localidade",
    )
    bai_no = models.CharField("nome do bairro", max_length=72)
    bai_no_abrev = models.CharField(
        "abreviatura do nome do bairro", max_length=36, null=True, blank=True
    )

    class Meta:
        managed = False
        # app_label intentionally uses the main app name so all CEP models
        # are grouped under a single section in Django admin
        app_label = "django_edne_cep"
        db_table = get_table_name("log_bairro")

    def __str__(self) -> str:
        return f"{self.bai_no} ({self.ufe_sg})"


class CaixaPostalComunitaria(models.Model):
    """Caixa Postal Comunitária (CPC)."""

    cpc_nu = models.AutoField("chave da CPC", primary_key=True)
    ufe_sg = models.CharField("sigla da UF", max_length=2)
    loc_nu = models.ForeignKey(
        Localidade,
        models.DO_NOTHING,
        db_column="loc_nu",
        verbose_name="localidade",
    )
    cpc_no = models.CharField("nome da CPC", max_length=72)
    cpc_endereco = models.CharField("endereço da CPC", max_length=100)
    cep = models.CharField("CEP da CPC", max_length=8)

    class Meta:
        managed = False
        # app_label intentionally uses the main app name so all CEP models
        # are grouped under a single section in Django admin
        app_label = "django_edne_cep"
        db_table = get_table_name("log_cpc")

    def __str__(self) -> str:
        return f"{self.cpc_no} - {self.cep}"


class Logradouro(models.Model):
    """Logradouros."""

    log_nu = models.AutoField("chave do logradouro", primary_key=True)
    ufe_sg = models.CharField("sigla da UF", max_length=2)
    loc_nu = models.ForeignKey(
        Localidade,
        models.DO_NOTHING,
        db_column="loc_nu",
        verbose_name="localidade",
    )
    bai_nu_ini = models.ForeignKey(
        Bairro,
        models.DO_NOTHING,
        db_column="bai_nu_ini",
        verbose_name="bairro inicial do logradouro",
    )
    bai_nu_fim = models.ForeignKey(
        Bairro,
        models.DO_NOTHING,
        db_column="bai_nu_fim",
        verbose_name="bairro final do logradouro",
        related_name="logradouro_bai_nu_fim_set",
        null=True,
        blank=True,
    )
    log_no = models.CharField("nome do logradouro", max_length=100)
    log_complemento = models.CharField(
        "complemento", max_length=100, null=True, blank=True
    )
    cep = models.CharField("CEP do logradouro", max_length=8)
    tlo_tx = models.CharField("tipo de logradouro", max_length=36)
    log_sta_tlo = models.CharField(
        "utilização do tipo de logradouro",
        max_length=1,
        choices=SimNao.choices,
        null=True,
        blank=True,
    )
    log_no_abrev = models.CharField(
        "abreviatura do nome do logradouro", max_length=36, null=True, blank=True
    )

    class Meta:
        managed = False
        # app_label intentionally uses the main app name so all CEP models
        # are grouped under a single section in Django admin
        app_label = "django_edne_cep"
        db_table = get_table_name("log_logradouro")

    def __str__(self) -> str:
        return f"{self.log_no} - {self.cep}"


class GrandeUsuario(models.Model):
    """Grande usuário dos Correios."""

    gru_nu = models.AutoField("chave do grande usuário", primary_key=True)
    ufe_sg = models.CharField("sigla da UF", max_length=2)
    loc_nu = models.ForeignKey(
        Localidade,
        models.DO_NOTHING,
        db_column="loc_nu",
        verbose_name="localidade",
    )
    bai_nu = models.ForeignKey(
        Bairro,
        models.DO_NOTHING,
        db_column="bai_nu",
        verbose_name="bairro",
    )
    log_nu = models.ForeignKey(
        Logradouro,
        models.DO_NOTHING,
        db_column="log_nu",
        verbose_name="logradouro",
        null=True,
        blank=True,
    )
    gru_no = models.CharField("nome do grande usuário", max_length=72)
    gru_endereco = models.CharField("endereço do grande usuário", max_length=100)
    cep = models.CharField("CEP do grande usuário", max_length=8)
    gru_no_abrev = models.CharField(
        "abreviatura do nome do grande usuário", max_length=36, null=True, blank=True
    )

    class Meta:
        managed = False
        # app_label intentionally uses the main app name so all CEP models
        # are grouped under a single section in Django admin
        app_label = "django_edne_cep"
        db_table = get_table_name("log_grande_usuario")

    def __str__(self) -> str:
        return f"{self.gru_no} - {self.cep}"


class UnidadeOperacional(models.Model):
    """Unidade operacional dos Correios."""

    uop_nu = models.AutoField("chave da unidade operacional", primary_key=True)
    ufe_sg = models.CharField("sigla da UF", max_length=2)
    loc_nu = models.ForeignKey(
        Localidade,
        models.DO_NOTHING,
        db_column="loc_nu",
        verbose_name="localidade",
    )
    bai_nu = models.ForeignKey(
        Bairro,
        models.DO_NOTHING,
        db_column="bai_nu",
        verbose_name="bairro",
    )
    log_nu = models.ForeignKey(
        Logradouro,
        models.DO_NOTHING,
        db_column="log_nu",
        verbose_name="logradouro",
        null=True,
        blank=True,
    )
    uop_no = models.CharField("nome da unidade operacional", max_length=100)
    uop_endereco = models.CharField("endereço da unidade operacional", max_length=100)
    cep = models.CharField("CEP da unidade operacional", max_length=8)
    uop_in_cp = models.CharField(
        "caixa postal",
        max_length=1,
        choices=SimNao.choices,
        null=True,
        blank=True,
    )
    uop_no_abrev = models.CharField(
        "abreviatura do nome da unidade operacional",
        max_length=36,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        # app_label intentionally uses the main app name so all CEP models
        # are grouped under a single section in Django admin
        app_label = "django_edne_cep"
        db_table = get_table_name("log_unid_oper")

    def __str__(self) -> str:
        return f"{self.uop_no} - {self.cep}"
